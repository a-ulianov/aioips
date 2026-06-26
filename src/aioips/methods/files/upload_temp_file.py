"""Метод загрузки временного файла во временное хранилище IPS."""

from typing import Any

from ...core import APIManager


class UploadTempFileMixin(APIManager):
    """Реализует ``POST /core/api/files/temp`` (``Files_UploadTempFile``)."""

    async def upload_temp_file(
        self: "UploadTempFileMixin",
        file_data: bytes,
        file_name: str,
        *,
        is_already_packed: bool | None = None,
    ) -> str:
        """Загружает файл во временное хранилище сервера и возвращает его имя (МУТИРУЮЩАЯ).

        Первый шаг типового сценария прикрепления файла к объекту: содержимое
        отправляется как ``multipart/form-data`` во временное хранилище IPS, а сервер
        возвращает уникальное временное имя. Это временное имя затем передаётся в методы
        прикрепления к атрибутам объекта (``attachTempFiles``) или используется при
        создании объекта с файловыми атрибутами. Парный метод очистки —
        :meth:`delete_temp_file` (временные файлы следует удалять, если они не были
        прикреплены).

        Предусловий по состоянию объекта нет: загрузка во временное хранилище не
        затрагивает существующие объекты до явного прикрепления.

        Args:
            file_data: Содержимое файла в виде байтов (``bytes``). Отправляется как поле
                ``fileData`` формы.
            file_name: Имя файла (поле ``fileName``); сервер использует его как основу и
                может вернуть изменённое уникальное имя.
            is_already_packed: Флаг «файл уже упакован» (поле ``isAlreadyPacked``).
                ``None`` — поле не передаётся (поведение сервера по умолчанию).

        Returns:
            Уникальное имя временного файла, присвоенное сервером. Используется в
            последующих вызовах прикрепления; пустая строка означает отсутствие имени.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                temp_name = await ips.upload_temp_file(b"PDF-bytes", "schema.pdf")
                try:
                    ...  # прикрепить temp_name к атрибуту объекта
                finally:
                    await ips.delete_temp_file(temp_name)

        Notes:
            operationId ``Files_UploadTempFile``; путь ``POST /core/api/files/temp``
            (тело ``multipart/form-data``: ``fileName``, ``fileData``,
            опц. ``isAlreadyPacked``). Связанные: :meth:`delete_temp_file`.
        """
        multipart: list[dict[str, Any]] = [
            {"name": "fileName", "value": file_name},
            {
                "name": "fileData",
                "value": file_data,
                "filename": file_name,
                "content_type": "application/octet-stream",
            },
        ]
        if is_already_packed is not None:
            multipart.append({"name": "isAlreadyPacked", "value": str(is_already_packed).lower()})
        data = await self._request("post", "/core/api/files/temp", multipart=multipart)
        return "" if data is None else str(data)
