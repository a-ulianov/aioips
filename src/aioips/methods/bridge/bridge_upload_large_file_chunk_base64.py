"""Метод передачи части большого файла (Base64-строка) через IPS Bridge (мутация)."""

from typing import Any

from ...core import APIManager
from ...schemas.bridge.file_request import LargeFileChunkDTOBase64


class BridgeUploadLargeFileChunkBase64Mixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Files/UploadLargeFileChunkBase64``.

    ``operationId``: ``Bridge_UploadLargeFileChunkBase64``.
    """

    async def bridge_upload_large_file_chunk_base64(
        self: "BridgeUploadLargeFileChunkBase64Mixin",
        body: LargeFileChunkDTOBase64 | dict[str, Any] | None = None,
        *,
        confirm: bool = False,
    ) -> str:
        """Передаёт часть большого файла как Base64-строку в сессию (МУТАЦИЯ).

        IPS Bridge — серверный помощник десктоп-клиента; крупные файлы он
        принимает по частям. Метод — вариант
        :meth:`bridge_upload_large_file_chunk`, где ``data`` передаётся как
        обычная Base64-строка. Сессия открывается
        :meth:`bridge_upload_large_file_request`.

        Обратимость: незавершённую сессию закрывают отменой
        :meth:`bridge_upload_large_file_cancel` (по её GUID).

        Защита: пишет данные на сервер, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            body: Часть файла. Принимает :class:`LargeFileChunkDTOBase64` или
                ``dict`` с ключами ``requestGuid`` / ``chunkNumber`` / ``data``
                (Base64-строка). ``None`` — пустое тело ``{}``. Модель
                сериализуется ``by_alias`` + ``exclude_none``.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Строковый ответ сервера о приёме части (``str``). Пустая строка
            ``""``, если сервер вернул ``null``.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.bridge.file_request import LargeFileChunkDTOBase64
            async with IPSClient(config=config) as ips:
                await ips.bridge_upload_large_file_chunk_base64(
                    LargeFileChunkDTOBase64(
                        request_guid=guid, chunk_number=0, data="QUJD",
                    ),
                    confirm=True,
                )

        Notes:
            ``operationId``: ``Bridge_UploadLargeFileChunkBase64``; путь
            ``POST /core/api/Bridge/Files/UploadLargeFileChunkBase64``. Тело —
            ``LargeFileChunkDTOBase64``.
        """
        if confirm is not True:
            raise ValueError(
                "bridge_upload_large_file_chunk_base64 пишет данные на сервер; "
                "передайте confirm=True",
            )
        if body is None:
            payload: dict[str, Any] = {}
        elif isinstance(body, LargeFileChunkDTOBase64):
            payload = body.model_dump(mode="json", by_alias=True, exclude_none=True)
        else:
            payload = body
        data = await self._request(
            "post", "/core/api/Bridge/Files/UploadLargeFileChunkBase64", json=payload
        )
        return "" if data is None else str(data)
