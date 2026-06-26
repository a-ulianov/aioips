"""Метод получения файла объекта по идентификатору BLOB-записи."""

from ...core import APIManager


class ObjectFileByBlobIdMixin(APIManager):
    """Реализует ``GET /core/api/files/objects/{objectId}/files/{blobId}``.

    operationId ``Files_GetObjectFileByBlobId``.
    """

    async def object_file_by_blob_id(
        self: "ObjectFileByBlobIdMixin",
        object_id: int,
        blob_id: int,
    ) -> str:
        """Загружает содержимое файла объекта по идентификатору BLOB-записи.

        Однозначный способ получить конкретный файл объекта: ``blob_id``
        идентифицирует ровно одну запись о файле, поэтому в отличие от
        :meth:`object_file_by_name` нет неоднозначности при совпадающих именах.
        Значение ``blob_id`` берут из метаданных файла
        (:meth:`file_attributes` → ``file_info_collection`` → ``blob_id``).

        Предусловие по id-пространству: ``object_id`` — это идентификатор ОБЪЕКТА
        (``ObjectID`` / F_OBJECT_ID), а не идентификатор версии; ``blob_id`` —
        идентификатор записи о файле (BLOB-поля).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``ObjectID`` / F_OBJECT_ID).
            blob_id: Идентификатор записи о файле (``blob_id`` из метаданных
                файлового атрибута).

        Returns:
            Содержимое файла в виде строки. В swagger ответ описан как
            ``string`` с ``format: binary`` — тело файла, переданное текстом;
            для двоичных файлов это сырое содержимое, которое при необходимости
            кодируют в байты на стороне вызывающего кода.

        Raises:
            IPSNotFoundError: Если файл с таким ``blob_id`` у объекта не найден.
            IPSError: При иной ошибке ответа сервера.

        Example:
            async with IPSClient(config=config) as ips:
                content = await ips.object_file_by_blob_id(102550, 778899)
                # content — содержимое файла строкой

        Notes:
            operationId ``Files_GetObjectFileByBlobId``. Файлы хранятся во
            внешнем файловом хранилище (vault, диск X:). См. [[ips-object-model]].
        """
        path = f"/core/api/files/objects/{object_id}/files/{blob_id}"
        data = await self._request("get", path)
        return str(data)
