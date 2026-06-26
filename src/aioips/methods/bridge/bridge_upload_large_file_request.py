"""Метод инициализации чанковой загрузки файла через IPS Bridge (мутация)."""

from typing import Any

from ...core import APIManager
from ...schemas.bridge.file_request import LargeFileRequestDTO


class BridgeUploadLargeFileRequestMixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Files/UploadLargeFileRequest``.

    ``operationId``: ``Bridge_UploadLargeFileRequest``.
    """

    async def bridge_upload_large_file_request(
        self: "BridgeUploadLargeFileRequestMixin",
        body: LargeFileRequestDTO | dict[str, Any] | None = None,
        *,
        confirm: bool = False,
    ) -> str:
        """Открывает сессию чанковой загрузки большого файла (МУТАЦИЯ).

        IPS Bridge — серверный помощник десктоп-клиента; крупные файлы он
        принимает по частям. Метод инициирует загрузку, заявляя имя, размер и
        число частей, и возвращает GUID сессии. Далее части передают
        :meth:`bridge_upload_large_file_chunk` (или
        :meth:`bridge_upload_large_file_chunk_base64`); отмена —
        :meth:`bridge_upload_large_file_cancel`.

        Обратимость: открытую сессию закрывают отменой
        :meth:`bridge_upload_large_file_cancel` (передайте полученный GUID), а
        итоговый файл при необходимости — :meth:`bridge_delete_temp_stored_item`.

        Защита: начинает приём данных на сервере, поэтому защищена ``confirm`` —
        без ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            body: Параметры файла. Принимает :class:`LargeFileRequestDTO` или
                ``dict`` с ключами ``fileName`` / ``totalBytes`` / ``totalChunks``
                / ``customDirectoryPath``. ``None`` — пустое тело ``{}``. Модель
                сериализуется ``by_alias`` + ``exclude_none``.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            GUID сессии загрузки (``str``) для последующих чанков. Пустая строка
            ``""``, если сервер вернул ``null``.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.bridge.file_request import LargeFileRequestDTO
            async with IPSClient(config=config) as ips:
                guid = await ips.bridge_upload_large_file_request(
                    LargeFileRequestDTO(
                        file_name="big.bin", total_bytes=1024, total_chunks=2,
                    ),
                    confirm=True,
                )

        Notes:
            ``operationId``: ``Bridge_UploadLargeFileRequest``; путь
            ``POST /core/api/Bridge/Files/UploadLargeFileRequest``. Тело —
            ``LargeFileRequestDTO``.
        """
        if confirm is not True:
            raise ValueError(
                "bridge_upload_large_file_request начинает загрузку на сервер; "
                "передайте confirm=True",
            )
        if body is None:
            payload: dict[str, Any] = {}
        elif isinstance(body, LargeFileRequestDTO):
            payload = body.model_dump(mode="json", by_alias=True, exclude_none=True)
        else:
            payload = body
        data = await self._request(
            "post", "/core/api/Bridge/Files/UploadLargeFileRequest", json=payload
        )
        return "" if data is None else str(data)
