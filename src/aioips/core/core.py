"""Ядро клиента: единая точка выполнения авторизованных запросов к IPS Web API."""

import asyncio
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from types import TracebackType
from typing import Any, Literal

import aiohttp
from tenacity import (
    retry as tenacity_retry,
)
from tenacity import (
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from ..infrastructure.logging import get_logger
from .auth import AuthManager
from .config import IPSConfig
from .exceptions import (
    IPSConnectionError,
    IPSServerError,
    IPSTooManyRequestsError,
    exception_from_response,
)
from .observability import MetricsHook, RequestMetric
from .sessions import SessionManager

HttpMethod = Literal["get", "post", "put", "delete"]

# Тело JSON-запроса IPS: объект, массив (список id) или голая JSON-строка
# (напр. RTF-конвертеры, UpdateLaunchAction — сервер ждёт строку в теле).
JsonBody = dict[str, Any] | list[Any] | str | None


class APIManager:
    """Базовый класс клиента IPS: управляет сессией, авторизацией и запросами.

    Предоставляет защищённый метод :meth:`_request`, который используют все
    методы-разделы. Берёт на себя получение и обновление токена, повторы при
    транзиентных ошибках и преобразование ошибочных ответов в исключения.

    Используется как асинхронный контекстный менеджер::

        async with IPSClient(config=config) as ips:
            ...
    """

    def __init__(
        self,
        base_url: str | None = None,
        login_name: str | None = None,
        password: str | None = None,
        access_token: str | None = None,
        config: IPSConfig | None = None,
        *,
        metrics_hook: MetricsHook | None = None,
    ) -> None:
        """Инициализирует клиент IPS.

        Параметры-ярлыки (``base_url``, ``login_name``, ``password``,
        ``access_token``) удобны для быстрого старта; для полной настройки
        передайте готовый ``config``. Значения из аргументов имеют приоритет над
        переменными окружения.

        Args:
            base_url: Базовый URL сервера IPS Web API.
            login_name: Имя пользователя IPS.
            password: Пароль пользователя IPS.
            access_token: Заранее полученный JWT access-токен.
            config: Полная конфигурация клиента (альтернатива параметрам-ярлыкам).
            metrics_hook: Необязательный колбэк наблюдаемости
                (:data:`~aioips.core.observability.MetricsHook`), вызываемый после
                КАЖДОЙ попытки запроса с :class:`~aioips.core.observability.RequestMetric`
                (метод/путь/статус/длительность/попытка/ошибка). Для метрик/трейсинга
                (OpenTelemetry, Prometheus). Исключения хука глушатся.
        """
        self._config = config or self._build_config(
            base_url=base_url,
            login_name=login_name,
            password=password,
            access_token=access_token,
        )
        self._metrics_hook = metrics_hook
        self._logger = get_logger("core")
        self._closed = False
        self._sessions = SessionManager(
            timeout=self._config.request_timeout,
            connector_limit=self._config.connector_limit,
            verify_ssl=self._config.verify_ssl,
        )
        self._auth = AuthManager(self._config, self._raw_request, self._logger)

    @staticmethod
    def _build_config(**overrides: str | None) -> IPSConfig:
        """Собирает конфигурацию из переданных значений и окружения.

        Args:
            **overrides: Значения-ярлыки; ``None`` игнорируются.

        Returns:
            Готовый экземпляр :class:`IPSConfig`.
        """
        provided = {key: value for key, value in overrides.items() if value is not None}
        return IPSConfig(**provided)  # type: ignore[arg-type]

    @property
    def config(self) -> IPSConfig:
        """Конфигурация клиента."""
        return self._config

    @property
    def is_closed(self) -> bool:
        """Возвращает ``True``, если клиент закрыт."""
        return self._closed

    async def __aenter__(self) -> "APIManager":
        """Входит в асинхронный контекст.

        Raises:
            RuntimeError: Если клиент уже закрыт.
        """
        if self._closed:
            raise RuntimeError("Нельзя использовать закрытый клиент IPS")
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Освобождает ресурсы при выходе из контекста."""
        await self.close()

    async def close(self) -> None:
        """Закрывает HTTP-сессию клиента (идемпотентно)."""
        if self._closed:
            return
        self._closed = True
        await self._sessions.close()
        self._logger.debug("Клиент IPS закрыт")

    @staticmethod
    def _build_form_data(spec: list[dict[str, Any]]) -> aiohttp.FormData:
        """Строит свежий ``aiohttp.FormData`` из спецификации полей.

        Сборка выполняется заново на каждую попытку запроса, поэтому повтор
        (retry) безопасен — байтовое содержимое полей читается из памяти и не
        «расходуется» предыдущей попыткой.

        Args:
            spec: Список полей формы; каждое — словарь с ключами ``name``
                (имя поля), ``value`` (``bytes``/``str`` — содержимое) и
                необязательными ``filename`` и ``content_type``.

        Returns:
            Готовый объект ``aiohttp.FormData`` для ``multipart/form-data``.
        """
        form = aiohttp.FormData()
        for field in spec:
            form.add_field(
                field["name"],
                field["value"],
                filename=field.get("filename"),
                content_type=field.get("content_type"),
            )
        return form

    async def _raw_request(
        self,
        method: str,
        path: str,
        json: JsonBody = None,
        *,
        params: dict[str, Any] | None = None,
        token: str | None = None,
        multipart: list[dict[str, Any]] | None = None,
        raw_bytes: bool = False,
    ) -> tuple[int, Any]:
        """Выполняет одиночный HTTP-запрос без повторов и разбора ошибок.

        Используется менеджером авторизации и методом :meth:`_request`.

        Args:
            method: HTTP-метод.
            path: Путь эндпоинта, начинающийся со слеша.
            json: Тело запроса в формате JSON.
            params: Параметры строки запроса.
            token: Bearer-токен для заголовка ``Authorization``.
            multipart: Спецификация полей ``multipart/form-data`` (см.
                :meth:`_build_form_data`). Если задана — тело отправляется как
                форма, а параметр ``json`` игнорируется.
            raw_bytes: Если ``True`` и статус ответа < 400 — вернуть «сырые» байты
                тела (``bytes``) без разбора JSON (для бинарных загрузок: файлы,
                шрифты, контент документов). При ошибке (>= 400) тело по-прежнему
                разбирается как JSON для корректного маппинга исключений.

        Returns:
            Кортеж ``(http_status, parsed_body)``; тело может быть ``dict``,
            ``list``, ``bytes`` (при ``raw_bytes``) или ``None``.

        Raises:
            IPSConnectionError: При сетевой ошибке или таймауте.
        """
        url = f"{self._config.base_url}{path}"
        headers = {"Authorization": f"Bearer {token}"} if token else None
        session = self._sessions.get_session()
        request_kwargs: dict[str, Any] = {"params": params, "headers": headers}
        if multipart is not None:
            request_kwargs["data"] = self._build_form_data(multipart)
        else:
            request_kwargs["json"] = json
        try:
            async with session.request(method, url, **request_kwargs) as response:
                if raw_bytes and response.status < 400:
                    return response.status, await response.read()
                try:
                    data = await response.json(content_type=None)
                except (aiohttp.ContentTypeError, ValueError):
                    data = None
                return response.status, data
        except TimeoutError as exc:
            raise IPSConnectionError(0, "Таймаут запроса к IPS") from exc
        except (aiohttp.ClientError, ConnectionError, OSError) as exc:
            raise IPSConnectionError(0, f"Сетевая ошибка: {exc}") from exc

    def _create_retry(self) -> Any:
        """Создаёт tenacity-декоратор повторов на основе конфигурации."""
        return tenacity_retry(
            retry=retry_if_exception_type(
                (
                    IPSServerError,
                    IPSTooManyRequestsError,
                    IPSConnectionError,
                    asyncio.TimeoutError,
                )
            ),
            stop=stop_after_attempt(self._config.max_retries + 1),
            wait=wait_exponential(
                multiplier=1,
                min=self._config.retry_min_wait,
                max=self._config.retry_max_wait,
            ),
            reraise=True,
        )

    async def _request(
        self,
        method: HttpMethod,
        path: str,
        *,
        json: JsonBody = None,
        params: dict[str, Any] | None = None,
        multipart: list[dict[str, Any]] | None = None,
        raw_bytes: bool = False,
    ) -> Any:
        """Выполняет авторизованный запрос к IPS с повторами и разбором ошибок.

        При ответе ``401`` один раз обновляет токен и повторяет запрос.
        Транзиентные ошибки (5xx, 429, сетевые) повторяются с экспоненциальной
        задержкой согласно конфигурации.

        Args:
            method: HTTP-метод.
            path: Путь эндпоинта, начинающийся со слеша (например,
                ``/core/api/metadata/objectTypes``).
            json: Тело запроса в формате JSON.
            params: Параметры строки запроса.
            multipart: Спецификация полей ``multipart/form-data`` для загрузки
                файлов (см. :meth:`_build_form_data`); при наличии ``json``
                игнорируется. Пересобирается на каждой попытке — повтор безопасен.
            raw_bytes: Если ``True`` — вернуть «сырые» байты тела успешного ответа
                (для бинарных загрузок). Ошибки разбираются как JSON для маппинга.

        Returns:
            Разобранное тело ответа (``dict``/``list``) либо ``bytes`` при
            ``raw_bytes``.

        Raises:
            IPSAuthError: При ошибке авторизации (401).
            IPSClientError: При некорректном запросе (400).
            IPSForbiddenError: При запрете доступа (403).
            IPSNotFoundError: При отсутствии ресурса (404).
            IPSConflictError: При конфликте состояния (409).
            IPSTooManyRequestsError: При превышении лимита запросов (429).
            IPSServerError: При внутренней ошибке сервера (500).
            IPSConnectionError: При сетевой ошибке или таймауте.
        """
        if self._closed:
            raise RuntimeError("Клиент IPS закрыт")

        attempt_no = 0

        async def _attempt() -> Any:
            nonlocal attempt_no
            attempt_no += 1
            started = time.perf_counter()
            status: int | None = None
            error: BaseException | None = None
            try:
                token = await self._auth.ensure_access_token()
                status, data = await self._raw_request(
                    method,
                    path,
                    json,
                    params=params,
                    token=token,
                    multipart=multipart,
                    raw_bytes=raw_bytes,
                )

                if status == 401:
                    self._logger.debug("Получен 401, обновляем токен и повторяем запрос")
                    token = await self._auth.force_refresh()
                    status, data = await self._raw_request(
                        method,
                        path,
                        json,
                        params=params,
                        token=token,
                        multipart=multipart,
                        raw_bytes=raw_bytes,
                    )

                if status >= 400:
                    error_body = data if isinstance(data, dict) else None
                    raise exception_from_response(status, error_body)

                return data
            except BaseException as exc:
                error = exc
                raise
            finally:
                self._emit_metric(
                    method, path, status, (time.perf_counter() - started) * 1000, attempt_no, error
                )

        retry_decorator = self._create_retry()
        return await retry_decorator(_attempt)()

    def _emit_metric(
        self,
        method: str,
        path: str,
        status: int | None,
        duration_ms: float,
        attempt: int,
        error: BaseException | None,
    ) -> None:
        """Вызывает хук наблюдаемости, глуша его исключения (fail-safe)."""
        if self._metrics_hook is None:
            return
        try:
            self._metrics_hook(RequestMetric(method, path, status, duration_ms, attempt, error))
        except Exception:
            self._logger.debug("metrics_hook бросил исключение — проигнорировано", exc_info=True)

    @asynccontextmanager
    async def stream(
        self,
        method: HttpMethod,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: JsonBody = None,
        chunk_size: int = 65536,
    ) -> AsyncIterator[AsyncIterator[bytes]]:
        """Потоково скачивает тело ответа, НЕ загружая его целиком в память.

        Возвращает асинхронный контекстный менеджер, дающий итератор байтовых
        чанков. В отличие от обычных бинарных методов (которые читают весь файл в
        ``bytes``), подходит для больших файлов (приложение моста, контент
        документа) — память постоянна. Применяйте, когда размер файла велик или
        заранее неизвестен.

        Особенности (отличия от :meth:`_request`): запрос выполняется ОДИН раз,
        БЕЗ tenacity-повторов (поток нельзя безопасно перезапустить на середине);
        токен обновляется заранее (``ensure_access_token``), но 401 в полёте не
        перезапрашивается. Ошибки ответа (>= 400) поднимаются как исключения ДО
        выдачи чанков (тело ошибки разбирается как JSON для маппинга).

        Args:
            method: HTTP-метод (обычно ``"get"``).
            path: Путь эндпоинта, начинающийся со слеша.
            params: Параметры строки запроса.
            json: Тело запроса (если нужно), как в :meth:`_request`.
            chunk_size: Размер байтового чанка для итерации (по умолчанию 64 КиБ).

        Yields:
            Асинхронный итератор ``bytes`` — чанки тела ответа по порядку.

        Raises:
            RuntimeError: Если клиент закрыт.
            IPSError: При ошибочном ответе сервера (>= 400) — до выдачи чанков.
            IPSConnectionError: При сетевой ошибке или таймауте.

        Example:
            async with ips.stream(
                "get", "/core/api/Bridge/Download/App", params={"platformName": "win-x64"}
            ) as chunks:
                with open("bridge.exe", "wb") as f:
                    async for chunk in chunks:
                        f.write(chunk)
        """
        if self._closed:
            raise RuntimeError("Клиент IPS закрыт")
        token = await self._auth.ensure_access_token()
        url = f"{self._config.base_url}{path}"
        headers = {"Authorization": f"Bearer {token}"} if token else None
        session = self._sessions.get_session()
        try:
            async with session.request(
                method, url, params=params, json=json, headers=headers
            ) as response:
                if response.status >= 400:
                    try:
                        err = await response.json(content_type=None)
                    except (aiohttp.ContentTypeError, ValueError):
                        err = None
                    raise exception_from_response(
                        response.status, err if isinstance(err, dict) else None
                    )
                yield response.content.iter_chunked(chunk_size)
        except TimeoutError as exc:
            raise IPSConnectionError(0, "Таймаут потокового запроса к IPS") from exc
        except (aiohttp.ClientError, ConnectionError, OSError) as exc:
            raise IPSConnectionError(0, f"Сетевая ошибка потока: {exc}") from exc
