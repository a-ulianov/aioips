"""Схема описания объекта вместе с его файловыми атрибутами.

References:
    ``GET /core/api/files/objects/{objectId}`` — ``ObjectWithFileAttributesDto``
    (operationId ``Files_GetFileAttributes``).
"""

from datetime import datetime
from typing import Annotated

from pydantic import Field

from ...common.enumerations.attribute import FieldType
from ..base import EmptyListIfNone, IPSModel


class BlobFileAttributeInfo(IPSModel):
    """Метаданные одного файла (BLOB-записи) внутри файлового атрибута.

    Соответствует ``BlobInformation`` доменной модели: описывает один
    физический файл, хранящийся в файловом шкафу (vault) или как BLOB в БД.
    Сам контент здесь не передаётся — он загружается отдельно по ``blob_id``
    методом :meth:`object_file_by_blob_id` или по имени методом
    :meth:`object_file_by_name`.

    Обязательны все перечисленные поля (DTO помечает их required); ``arc_method``
    и ``file_type`` приходят строковыми значениями соответствующих перечислений
    IPS (``ArcMethods`` / ``FileTypes``) и моделируются как строки.

    Attributes:
        blob_id: Идентификатор записи о файле (BLOB-поля); DTO ``blobId``.
        real_file_size: Реальный (распакованный) размер файла в байтах
            (DTO ``realFileSize``).
        packed_file_size: Упакованный размер файла в байтах (DTO ``packedFileSize``).
        modify_date: Дата модификации файла в локальном времени, округлённая до
            секунд (DTO ``modifyDate``).
        file_name: Имя файла (для чистого BLOB-поля пусто); DTO ``fileName``.
        arc_method: Метод запаковки (``ArcMethods``): ``notPacked`` / ``zLibPacked``
            / ``zstd`` (DTO ``arcMethod``).
        note: Комментарий к файлу (только для хранящихся в файловом хранилище);
            DTO ``note``.
        file_type: Тип файла (``FileTypes``): ``ftNormal`` / ``ftNotContent`` /
            ``ftOTD`` / ``ftRedlining`` / ``ftAuthentical`` / ``ftUnknown``
            (DTO ``fileType``).
        author_id: Автор файла (``ObjectID``); DTO ``authorId``.
        file_storage_id: Файловый шкаф (``ObjectID``); DTO ``fileStorageId``.
    """

    blob_id: int = Field(description="Идентификатор записи о файле (BLOB-поля)")
    real_file_size: int = Field(description="Реальный размер файла в байтах")
    packed_file_size: int = Field(description="Упакованный размер файла в байтах")
    modify_date: datetime = Field(description="Дата модификации файла (локальное время)")
    file_name: str = Field(description="Имя файла (для BLOB-поля пусто)")
    arc_method: str = Field(description="Метод запаковки (ArcMethods)")
    note: str = Field(description="Комментарий к файлу")
    file_type: str = Field(description="Тип файла (FileTypes)")
    author_id: int = Field(description="Автор файла (ObjectID)")
    file_storage_id: int = Field(description="Файловый шкаф (ObjectID)")


class FileAttribute(IPSModel):
    """Один файловый атрибут объекта вместе со списком вложенных файлов.

    Описывает атрибут типа ``ftFile`` (или иной файловый тип) у конкретного
    объекта: его идентификатор, тип данных, признак множественности и набор
    физических файлов (:class:`BlobFileAttributeInfo`), которые в нём хранятся.

    Attributes:
        attribute_id: Идентификатор атрибута (DTO ``attributeId``).
        attribute_field_type: Тип данных атрибута (``FieldTypes``); DTO
            ``attributeFieldType``. Для файловых атрибутов — обычно ``ftFile``.
        is_multiple: Может ли атрибут содержать несколько файлов
            (DTO ``isMultiple``).
        file_info_collection: Список метаданных файлов атрибута
            (DTO ``fileInfoCollection``); может прийти ``null`` → пустой список.
        read_only: Признак «только для чтения» для атрибута (DTO ``readOnly``).
    """

    attribute_id: int = Field(description="Идентификатор атрибута")
    attribute_field_type: FieldType = Field(description="Тип данных атрибута")
    is_multiple: bool = Field(description="Может ли атрибут содержать несколько файлов")
    file_info_collection: Annotated[list[BlobFileAttributeInfo], EmptyListIfNone] = Field(
        default_factory=list, description="Метаданные файлов атрибута"
    )
    read_only: bool = Field(description="Признак «только для чтения» атрибута")


class ObjectWithFileAttributes(IPSModel):
    """Объект (его версия) вместе со всеми его файловыми атрибутами.

    Результат :meth:`file_attributes`: компактное представление объекта,
    сфокусированное на файлах. Содержит идентификатор версии объекта, его тип,
    признак «только для чтения» и список файловых атрибутов
    (:class:`FileAttribute`), каждый из которых перечисляет хранящиеся в нём
    файлы. Контент файлов не включён — он загружается отдельными методами.

    Предусловие по id-пространству: ``object_version_id`` — это идентификатор
    ВЕРСИИ объекта (F_ID), а не идентификатор объекта (``ObjectID``). Сами
    методы раздела принимают ``ObjectID``, а сервер возвращает версию объекта.

    Attributes:
        object_version_id: Идентификатор версии объекта (F_ID); DTO
            ``objectVersionId``.
        object_type: Идентификатор типа объекта (DTO ``objectType``).
        read_only: Признак «только для чтения» объекта (DTO ``readOnly``).
        attributes: Список файловых атрибутов объекта (DTO ``attributes``);
            может прийти ``null`` → пустой список.
    """

    object_version_id: int = Field(description="Идентификатор версии объекта (F_ID)")
    object_type: int = Field(description="Идентификатор типа объекта")
    read_only: bool = Field(description="Признак «только для чтения» объекта")
    attributes: Annotated[list[FileAttribute], EmptyListIfNone] = Field(
        default_factory=list, description="Файловые атрибуты объекта"
    )
