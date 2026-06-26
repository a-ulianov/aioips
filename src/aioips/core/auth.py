"""Управление жизненным циклом JWT-токена авторизации IPS.

Схема авторизации IPS Web API (двухшаговая):

1. ``GET /core/api/Auth/logins/{loginName}/options`` — доступные роли и уровни
   доступа для логина (без пароля).
2. ``POST /core/api/Auth/authenticate`` — обмен логина/пароля на пару токенов
   ``{accessToken, refreshToken, expireTime}``.
3. Обновление: ``POST /core/api/Auth/refreshTokens`` — обмен текущей пары на новую.

References:
    Эндпоинты ``/core/api/Auth/*`` сервера IPS Server Web API.
"""

import asyncio
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from logging import Logger
from typing import Any
from urllib.parse import quote

from .config import IPSConfig
from .exceptions import IPSAuthError, exception_from_response

# Низкоуровневый запрос: (method, path, json) -> (status, data).
RawResponse = tuple[int, dict[str, Any] | None]
RawRequest = Callable[[str, str, dict[str, Any] | None], Awaitable[RawResponse]]


class AuthManager:
    """Получает и обновляет JWT-токен для доступа к IPS Web API.

    Менеджер потокобезопасен относительно конкурентных корутин: одновременные
    обращения к :meth:`ensure_access_token` не приводят к повторной аутентификации.
    """

    def __init__(self, config: IPSConfig, raw_request: RawRequest, logger: Logger) -> None:
        """Инициализирует менеджер авторизации.

        Args:
            config: Конфигурация клиента с авторизационными данными.
            raw_request: Низкоуровневая корутина выполнения HTTP-запроса без авторизации.
            logger: Логгер для диагностических сообщений.
        """
        self._config = config
        self._raw_request = raw_request
        self._logger = logger
        self._lock = asyncio.Lock()

        self._access_token: str | None = config.access_token
        self._refresh_token: str | None = None
        self._expire_time: datetime | None = None

    @property
    def access_token(self) -> str | None:
        """Текущий access-токен (без гарантии актуальности)."""
        return self._access_token

    async def login_options(self, login_name: str) -> dict[str, Any]:
        """Возвращает доступные роли и уровни доступа для логина (без пароля).

        Args:
            login_name: Имя пользователя IPS.

        Returns:
            Тело ответа ``AuthOptionsDTO``: ключи ``roles`` и ``accessLevels``.

        Raises:
            IPSError: При ошибочном ответе сервера.
        """
        path = f"/core/api/Auth/logins/{quote(login_name, safe='')}/options"
        status, data = await self._raw_request("get", path, None)
        if status >= 400 or data is None:
            raise exception_from_response(status, data)
        return data

    async def ensure_access_token(self) -> str:
        """Возвращает действующий access-токен, при необходимости получая/обновляя его.

        Returns:
            Действующий JWT access-токен.

        Raises:
            IPSAuthError: Если авторизация не удалась.
        """
        async with self._lock:
            if self._access_token is None:
                await self._authenticate_locked()
            elif self._is_expired():
                await self._refresh_or_reauth_locked()
            token = self._access_token
        if token is None:  # pragma: no cover - защитный инвариант
            raise IPSAuthError(401, "Не удалось получить access-токен")
        return token

    async def force_refresh(self) -> str:
        """Принудительно обновляет токен (например, после ответа 401).

        Returns:
            Свежий access-токен.

        Raises:
            IPSAuthError: Если обновление и повторная аутентификация невозможны.
        """
        async with self._lock:
            await self._refresh_or_reauth_locked()
            token = self._access_token
        if token is None:  # pragma: no cover - защитный инвариант
            raise IPSAuthError(401, "Не удалось обновить access-токен")
        return token

    def _is_expired(self) -> bool:
        """Проверяет, истёк ли токен с учётом запаса ``token_refresh_skew``."""
        if self._expire_time is None:
            return False
        remaining = (self._expire_time - datetime.now(UTC)).total_seconds()
        return remaining <= self._config.token_refresh_skew

    async def _refresh_or_reauth_locked(self) -> None:
        """Обновляет токен через refresh, при неудаче — повторно аутентифицируется."""
        if self._refresh_token is not None:
            try:
                await self._refresh_locked()
                return
            except IPSAuthError:
                self._logger.debug("Refresh не удался, выполняем повторную аутентификацию")
        await self._authenticate_locked()

    async def _authenticate_locked(self) -> None:
        """Выполняет первичную аутентификацию по логину и паролю.

        Raises:
            IPSAuthError: Если для аутентификации нет логина/пароля или сервер отказал.
        """
        if not (self._config.login_name and self._config.password):
            raise IPSAuthError(401, "Токен истёк, а логин/пароль для повторного входа не заданы")

        role_id = await self._resolve_role_id()
        payload: dict[str, Any] = {
            "loginName": self._config.login_name,
            "password": self._config.password,
            "passwordType": self._config.password_type,
            "roleID": role_id,
            "accessLevelID": self._config.access_level_id,
        }
        status, data = await self._raw_request("post", "/core/api/Auth/authenticate", payload)
        if status >= 400 or data is None:
            raise exception_from_response(status, data)
        self._store_tokens(data)
        self._logger.debug("Выполнена аутентификация в IPS")

    async def _refresh_locked(self) -> None:
        """Обновляет пару токенов через ``/core/api/Auth/refreshTokens``.

        Raises:
            IPSAuthError: Если сервер отклонил обновление.
        """
        payload: dict[str, Any] = {
            "accessToken": self._access_token,
            "refreshToken": self._refresh_token,
            "expireTime": self._expire_time.isoformat() if self._expire_time else None,
        }
        status, data = await self._raw_request("post", "/core/api/Auth/refreshTokens", payload)
        if status >= 400 or data is None:
            raise exception_from_response(status, data)
        self._store_tokens(data)
        self._logger.debug("Токен IPS обновлён")

    async def _resolve_role_id(self) -> int:
        """Определяет идентификатор роли для аутентификации.

        Использует ``role_id`` из конфигурации; если задано только ``role_name`` —
        резолвит его через ``login options``. Если роль не задана вовсе, берёт 0
        (сервер выберет роль по умолчанию).

        Returns:
            Числовой идентификатор роли.

        Raises:
            IPSAuthError: Если указанное имя роли недоступно для логина.
        """
        if self._config.role_id is not None:
            return self._config.role_id
        if self._config.role_name is None:
            return 0

        login_name = self._config.login_name
        if login_name is None:  # pragma: no cover - вызывается только при наличии логина
            raise IPSAuthError(401, "Для резолвинга роли требуется имя пользователя")

        options = await self.login_options(login_name)
        for role in options.get("roles", []):
            if role.get("name") == self._config.role_name:
                role_id: int = role["id"]
                return role_id

        available = ", ".join(r.get("name", "?") for r in options.get("roles", []))
        raise IPSAuthError(
            401,
            f"Роль '{self._config.role_name}' недоступна. Доступные роли: {available}",
        )

    def _store_tokens(self, data: dict[str, Any]) -> None:
        """Сохраняет полученную пару токенов и время истечения."""
        self._access_token = data.get("accessToken")
        self._refresh_token = data.get("refreshToken")
        self._expire_time = self._parse_expire_time(data.get("expireTime"))

    @staticmethod
    def _parse_expire_time(value: str | None) -> datetime | None:
        """Разбирает ISO 8601 строку времени истечения токена в ``datetime`` (UTC)."""
        if not value:
            return None
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return parsed
