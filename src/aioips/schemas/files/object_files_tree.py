"""Схема узла дерева файлов объекта с учётом состава (ёлочка) IPS Web API.

References:
    DTO ``ObjectFilesTreeNodeDto`` — ответ
    ``POST /core/api/files/objects/{objectId}/withComposition``
    (operationId ``Files_GetFileInfoForObjectWithComposition``).
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class ObjectFilesTreeNodeDto(IPSModel):
    """Узел дерева файлов объекта с рекурсивным разворачиванием состава.

    Описывает один объект и его файлы в дереве «ёлочка»: корневой узел — это
    запрошенный объект, а :attr:`child_nodes` — узлы объектов-компонентов состава
    (рекурсивно, на любую глубину). Возвращается методом
    ``object_files_with_composition`` для обхода всех файлов сборки/изделия
    вместе с файлами входящих в неё деталей одним запросом. Это операция ЧТЕНИЯ.

    Предусловие по id-пространству: :attr:`object_id` — это ``ObjectID``
    (F_OBJECT_ID, общий для версий), а не ``id`` версии.

    Attributes:
        object_id: Идентификатор ОБЪЕКТА узла (DTO ``objectId`` / ``ObjectID``,
            int64).
        caption: Подпись (имя/наименование) объекта (DTO ``caption``). ``None`` —
            подпись отсутствует.
        file_info_collection: Информация о файлах объекта (DTO
            ``fileInfoCollection``) — массив ``BlobFileAttributeInfoDto``,
            отдаваемый как список словарей (значимые ключи: ``blobId``,
            ``fileName``, ``fileType``, ``realFileSize``, ``modifyDate``,
            ``fileStorageId``). ``null`` от сервера → ``[]``.
        child_nodes: Дочерние узлы — объекты состава данного объекта (DTO
            ``childNodes``), та же схема рекурсивно. ``null`` → ``[]``.
    """

    object_id: int = Field(default=0, description="Идентификатор объекта узла (ObjectID)")
    caption: str | None = Field(default=None, description="Подпись объекта")
    file_info_collection: Annotated[list[dict[str, Any]], EmptyListIfNone] = Field(
        default_factory=list, description="Информация о файлах (BlobFileAttributeInfoDto)"
    )
    child_nodes: Annotated[list["ObjectFilesTreeNodeDto"], EmptyListIfNone] = Field(
        default_factory=list, description="Дочерние узлы состава (рекурсивно)"
    )


ObjectFilesTreeNodeDto.model_rebuild()
