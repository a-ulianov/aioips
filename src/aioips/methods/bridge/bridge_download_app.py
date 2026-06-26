"""Метод загрузки дистрибутива приложения IPS Bridge (бинарное чтение)."""

from typing import Any

from ...core import APIManager


class BridgeDownloadAppMixin(APIManager):
    """Реализует ``GET /core/api/Bridge/Download/App``.

    operationId ``Bridge_DownloadBridgeApp``.
    """

    async def bridge_download_app(
        self: "BridgeDownloadAppMixin",
        platform_name: str,
    ) -> bytes:
        """Скачивает дистрибутив приложения IPS Bridge для указанной платформы (БАЙТЫ).

        IPS Bridge — серверный помощник десктоп-клиента; этот метод отдаёт его
        установочный пакет (исполняемый/архивный файл) для конкретной платформы.
        Применяйте, когда нужно доставить или обновить мост на рабочем месте
        пользователя. Операция идемпотентна и не мутирует сервер.

        Возврат — «сырые» ``bytes`` тела ответа (бинарный файл,
        ``application/octet-stream``), а НЕ JSON: ядро вызывается с
        ``raw_bytes=True``. Сохраняйте результат как файл без перекодирования.

        Args:
            platform_name: Имя целевой платформы (передаётся в query как
                ``platformName``). Значение зависит от сервера (например,
                идентификатор ОС/архитектуры). Обязательный параметр.

        Returns:
            Содержимое дистрибутива как ``bytes``. Пустой ответ сервера —
            ``b""``.

        Raises:
            IPSNotFoundError: Если дистрибутив для платформы не найден.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                blob = await ips.bridge_download_app("win-x64")
                with open("ips-bridge.exe", "wb") as fh:
                    fh.write(blob)

        Notes:
            operationId ``Bridge_DownloadBridgeApp``; путь
            ``GET /core/api/Bridge/Download/App``; ключ query — ``platformName``.
            Бинарный ответ (``raw_bytes=True``). Связанные методы:
            :meth:`bridge_download_library`,
            :meth:`bridge_download_integrated_app_plugin`.
        """
        params: dict[str, Any] = {"platformName": platform_name}
        data = await self._request(
            "get",
            "/core/api/Bridge/Download/App",
            params=params,
            raw_bytes=True,
        )
        return data if isinstance(data, bytes) else b""
