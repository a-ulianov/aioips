"""Метод передачи части большого файла через IPS Bridge (мутация)."""

from typing import Any

from ...core import APIManager
from ...schemas.bridge.file_request import LargeFileChunkDTO


class BridgeUploadLargeFileChunkMixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Files/UploadLargeFileChunk``.

    ``operationId``: ``Bridge_UploadLargeFileChunk``.
    """

    async def bridge_upload_large_file_chunk(
        self: "BridgeUploadLargeFileChunkMixin",
        body: LargeFileChunkDTO | dict[str, Any] | None = None,
        *,
        confirm: bool = False,
    ) -> str:
        """Передаёт одну часть большого файла в открытую сессию загрузки (МУТАЦИЯ).

        IPS Bridge — серверный помощник десктоп-клиента; крупные файлы он
        принимает по частям. Метод отправляет очередной чанк (бинарные данные в
        Base64) в сессию, открытую :meth:`bridge_upload_large_file_request`.
        Вариант с обычной Base64-строкой —
        :meth:`bridge_upload_large_file_chunk_base64`.

        Обратимость: незавершённую сессию закрывают отменой
        :meth:`bridge_upload_large_file_cancel` (по её GUID).

        Защита: пишет данные на сервер, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            body: Часть файла. Принимает :class:`LargeFileChunkDTO` или ``dict`` с
                ключами ``requestGuid`` / ``chunkNumber`` / ``data`` (Base64).
                ``None`` — пустое тело ``{}``. Модель сериализуется ``by_alias`` +
                ``exclude_none``.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Строковый ответ сервера о приёме части (``str``). Пустая строка
            ``""``, если сервер вернул ``null``.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.bridge.file_request import LargeFileChunkDTO
            async with IPSClient(config=config) as ips:
                await ips.bridge_upload_large_file_chunk(
                    LargeFileChunkDTO(
                        request_guid=guid, chunk_number=0, data="QUJD",
                    ),
                    confirm=True,
                )

        Notes:
            ``operationId``: ``Bridge_UploadLargeFileChunk``; путь
            ``POST /core/api/Bridge/Files/UploadLargeFileChunk``. Тело —
            ``LargeFileChunkDTO``.
        """
        if confirm is not True:
            raise ValueError(
                "bridge_upload_large_file_chunk пишет данные на сервер; передайте confirm=True",
            )
        if body is None:
            payload: dict[str, Any] = {}
        elif isinstance(body, LargeFileChunkDTO):
            payload = body.model_dump(mode="json", by_alias=True, exclude_none=True)
        else:
            payload = body
        data = await self._request(
            "post", "/core/api/Bridge/Files/UploadLargeFileChunk", json=payload
        )
        return "" if data is None else str(data)
