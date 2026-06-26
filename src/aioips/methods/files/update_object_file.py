"""Метод замены содержимого файла в файловом атрибуте объекта."""

from datetime import datetime
from typing import Any

from ...core import APIManager
from ...schemas.files.object_with_file_attributes import BlobFileAttributeInfo


class UpdateObjectFileMixin(APIManager):
    """Реализует ``PUT /core/api/files/objects/{objectId}/files`` (multipart).

    operationId ``Files_UpdateObjectFile``.
    """

    async def update_object_file(
        self: "UpdateObjectFileMixin",
        object_id: int,
        attribute_id: int,
        blob_id: int,
        file_data: bytes,
        file_name: str,
        modify_date_time: datetime,
        *,
        real_file_size: int | None = None,
    ) -> BlobFileAttributeInfo:
        """Заменяет СОДЕРЖИМОЕ уже прикреплённого файла объекта (МУТИРУЮЩАЯ).

        Перезаписывает байты конкретного файла (адресуемого ``blob_id``) в
        файловом атрибуте объекта новым содержимым, передаваемым как
        ``multipart/form-data``. В отличие от :meth:`add_object_file` здесь не
        создаётся новая запись, а обновляется существующая; в отличие от
        :meth:`update_object_file_info` (правит только имя/комментарий) — здесь
        заменяется само содержимое файла. ``file_type`` при замене не передаётся
        (тип остаётся прежним).

        Предусловия: правка файлового атрибута обычно требует, чтобы объект был
        в режиме изменения (``checkOut`` → правка → ``checkIn``; см.
        ``ObjectModifyModes`` в объектной модели IPS). Файл с указанным
        ``blob_id`` должен уже существовать у объекта в этом атрибуте.

        Предусловие по id-пространству: ``object_id`` — идентификатор ОБЪЕКТА
        (``ObjectID`` / F_OBJECT_ID); ``attribute_id`` — идентификатор файлового
        атрибута (``ftFile``); ``blob_id`` — идентификатор существующей
        BLOB-записи (из ответа :meth:`add_object_file` или из метаданных
        :meth:`file_attributes`).

        Args:
            object_id: Идентификатор РАБОЧЕЙ КОПИИ объекта (результат
                :meth:`object_check_out`; на проде отрицательный), НЕ базовый
                ``ObjectID`` — объект должен быть взят на изменение, иначе сервер
                вернёт 400 «выполните checkOut».
            attribute_id: Идентификатор файлового атрибута (``ftFile``); поле
                формы ``attributeId`` (строкой).
            blob_id: Идентификатор заменяемой BLOB-записи; поле формы ``blobId``
                (строкой).
            file_data: Новое содержимое файла (``bytes``); поле ``fileData`` с
                ``filename=file_name`` и ``content_type=application/octet-stream``.
            file_name: Имя файла; поле формы ``fileName``.
            modify_date_time: Дата модификации файла (``datetime``); ISO-строка
                (``.isoformat()``) в поле формы ``modifyDateTime``.
            real_file_size: Реальный (распакованный) размер файла в байтах;
                необязательный query-параметр ``realFileSize``. ``None`` — не
                передаётся.

        Returns:
            :class:`BlobFileAttributeInfo` — обновлённые метаданные BLOB-записи
            (``blob_id``, размеры, дата модификации и т. д.).

        Raises:
            IPSNotFoundError: Если файл с таким ``blob_id`` у объекта не найден.
            IPSError: При иной ошибке сервера (объект не взят на изменение,
                атрибут только для чтения).

        Example:
            from datetime import datetime

            async with IPSClient(config=config) as ips:
                info = await ips.update_object_file(
                    object_id=102550,
                    attribute_id=1031,
                    blob_id=778899,
                    file_data=b"%PDF-1.4 new ...",
                    file_name="schema.pdf",
                    modify_date_time=datetime.utcnow(),
                )

        Notes:
            operationId ``Files_UpdateObjectFile``; путь ``PUT
            /core/api/files/objects/{objectId}/files`` (тело
            ``multipart/form-data``, без ``fileType``). Связанные:
            :meth:`add_object_file`, :meth:`update_object_file_info`,
            :meth:`delete_object_file`. См. объектной модели IPS.
        """
        multipart: list[dict[str, Any]] = [
            {"name": "attributeId", "value": str(attribute_id)},
            {"name": "blobId", "value": str(blob_id)},
            {"name": "fileName", "value": file_name},
            {"name": "modifyDateTime", "value": modify_date_time.isoformat()},
            {
                "name": "fileData",
                "value": file_data,
                "filename": file_name,
                "content_type": "application/octet-stream",
            },
        ]
        params: dict[str, Any] | None = None
        if real_file_size is not None:
            params = {"realFileSize": int(real_file_size)}
        path = f"/core/api/files/objects/{object_id}/files"
        data = await self._request("put", path, params=params, multipart=multipart)
        return BlobFileAttributeInfo.model_validate(data)
