"""Метод получения файла объекта по имени файла."""

from urllib.parse import quote

from ...core import APIManager


class ObjectFileByNameMixin(APIManager):
    """Реализует ``GET /core/api/files/objects/{objectId}/files/byName/{fileName}``.

    operationId ``Files_GetObjectFileByName``.
    """

    async def object_file_by_name(
        self: "ObjectFileByNameMixin",
        object_id: int,
        file_name: str,
    ) -> str:
        """Загружает содержимое файла объекта, выбранного по его имени.

        Применяют, когда имя файла известно (например, из
        :meth:`file_attributes`, поле ``file_name``), а идентификатор записи
        (``blob_id``) — нет. Если у объекта несколько файлов с одинаковым именем,
        однозначнее обращаться по ``blob_id`` через
        :meth:`object_file_by_blob_id`.

        Предусловие по id-пространству: ``object_id`` — это идентификатор ОБЪЕКТА
        (``ObjectID`` / F_OBJECT_ID), а не идентификатор версии. Имя файла
        URL-кодируется автоматически (через ``quote``), поэтому передавайте его
        как есть, без предварительного экранирования.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``ObjectID`` / F_OBJECT_ID).
            file_name: Имя файла внутри файлового атрибута объекта (как в поле
                ``file_name`` метаданных). Кодируется в URL автоматически.

        Returns:
            Содержимое файла в виде строки. В swagger ответ описан как
            ``string`` с ``format: binary`` — то есть тело файла, переданное
            текстом; для двоичных файлов это сырое содержимое, которое при
            необходимости кодируют в байты на стороне вызывающего кода.

        Raises:
            IPSNotFoundError: Если файл с таким именем у объекта не найден.
            IPSError: При иной ошибке ответа сервера.

        Example:
            async with IPSClient(config=config) as ips:
                content = await ips.object_file_by_name(102550, "specification.pdf")
                # content — содержимое файла строкой

        Notes:
            operationId ``Files_GetObjectFileByName``. Файлы хранятся во внешнем
            файловом хранилище (vault, диск X:). См. [[ips-object-model]].
        """
        encoded_name = quote(file_name, safe="")
        path = f"/core/api/files/objects/{object_id}/files/byName/{encoded_name}"
        data = await self._request("get", path)
        return str(data)
