"""Метод загрузки файла во временное хранилище IPS Bridge (мутация)."""

from typing import Any

from ...core import APIManager
from ...schemas.bridge.file_request import FileRequestDTO


class BridgeUploadFileMixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Files/UploadFile``.

    ``operationId``: ``Bridge_UploadFile``.
    """

    async def bridge_upload_file(
        self: "BridgeUploadFileMixin",
        body: FileRequestDTO | dict[str, Any] | None = None,
        *,
        confirm: bool = False,
    ) -> str:
        """Загружает файл целиком во временное хранилище сессии (МУТАЦИЯ).

        IPS Bridge — серверный помощник десктоп-клиента; он принимает файлы во
        временное хранилище сессии. Метод загружает небольшой файл одним
        запросом (содержимое — Base64 в ``data``) и возвращает серверный путь.
        Для крупных файлов используйте чанковую загрузку:
        :meth:`bridge_upload_large_file_request` →
        :meth:`bridge_upload_large_file_chunk`.

        Обратимость: операция создаёт файл; уберите его парным
        :meth:`bridge_delete_temp_stored_item` по возвращённому пути.

        Защита: создаёт файл на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            body: Описание файла. Принимает :class:`FileRequestDTO` или ``dict``
                с ключами ``data`` (Base64) / ``fileName`` / ``content``. ``None``
                — отправляется пустое тело ``{}``. Модель сериализуется
                ``by_alias`` + ``exclude_none``.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Серверный путь загруженного файла (``str``). Пустая строка ``""``,
            если сервер вернул ``null``.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.bridge.file_request import FileRequestDTO
            async with IPSClient(config=config) as ips:
                path = await ips.bridge_upload_file(
                    FileRequestDTO(data="QUJD", file_name="a.txt"), confirm=True,
                )

        Notes:
            ``operationId``: ``Bridge_UploadFile``; путь
            ``POST /core/api/Bridge/Files/UploadFile``. Тело — ``FileRequestDTO``.
        """
        if confirm is not True:
            raise ValueError(
                "bridge_upload_file загружает файл на сервер; передайте confirm=True",
            )
        if body is None:
            payload: dict[str, Any] = {}
        elif isinstance(body, FileRequestDTO):
            payload = body.model_dump(mode="json", by_alias=True, exclude_none=True)
        else:
            payload = body
        data = await self._request("post", "/core/api/Bridge/Files/UploadFile", json=payload)
        return "" if data is None else str(data)
