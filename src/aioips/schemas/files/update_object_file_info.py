"""Схема обновления метаинформации файла объекта (без перезаписи содержимого).

References:
    ``PUT /core/api/files/objects/{objectId}/files/info`` —
    ``UpdateObjectFileInfoDto`` (operationId ``Files_UpdateObjectFileInfo``).
"""

from pydantic import Field

from ..base import IPSModel


class UpdateObjectFileInfo(IPSModel):
    """Параметры правки атрибутов одного файла (BLOB-записи) объекта.

    Тело запроса :meth:`update_object_file_info`: позволяет изменить ИМЯ файла
    и/или КОММЕНТАРИЙ к нему, не перезаписывая само содержимое. В отличие от
    :meth:`update_object_file` (который заменяет байты файла новым контентом),
    этот DTO правит только метаданные записи о файле. Конкретный файл адресуется
    парой ``attribute_id`` + ``blob_id``.

    Предусловие по id-пространству: ``blob_id`` — идентификатор записи о файле
    (BLOB-поля), полученный из ответа :meth:`add_object_file` или из метаданных
    :meth:`file_attributes`; ``attribute_id`` — идентификатор файлового атрибута
    (тип ``ftFile``), в котором лежит файл. Оба обязательны на стороне сервера;
    ``file_name`` и ``note`` опциональны — ``None`` исключается из тела при
    сериализации (поле не отправляется, текущее значение на сервере сохраняется).

    Attributes:
        blob_id: Идентификатор записи о файле (BLOB-поля); DTO ``blobId``,
            int64. Обязателен серверу.
        attribute_id: Идентификатор файлового атрибута (``ftFile``); DTO
            ``attributeId``, int32. Обязателен серверу.
        file_name: Новое имя файла; DTO ``fileName``. ``None`` — имя не меняется
            (поле не отправляется).
        note: Новый комментарий к файлу; DTO ``note``. ``None`` — комментарий не
            меняется (поле не отправляется).
    """

    blob_id: int = Field(default=0, description="Идентификатор записи о файле (BLOB-поля)")
    attribute_id: int = Field(default=0, description="Идентификатор файлового атрибута (ftFile)")
    file_name: str | None = Field(default=None, description="Новое имя файла")
    note: str | None = Field(default=None, description="Новый комментарий к файлу")
