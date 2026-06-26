"""Схемы информационного объекта IPS.

Информационный объект — основная единица данных IPS (изделие, документ, элемент состава
и т.п.). Каждый объект существует в виде версий; идентичность задаётся парой
«идентификатор версии» и «GUID версии», а сам объект — отдельным GUID объекта.

Внимание: IPS сериализует имена .NET-свойств с заглавными суффиксами-акронимами
(``objectID``, ``versionID``, ``objectGUID``), причём непоследовательно между DTO. Поэтому
для таких полей задаём явные алиасы, равные точному ключу JSON (см. [[gotchas]]).

См. [[ips-object-model]] (раздел «Идентичность: объект ≠ версия») и [[gotchas]].

References:
    ``GET /core/api/objects/{objectId}`` — ``Objects_GetObject`` (``ObjectDto``).
    ``POST /core/api/objects/collection`` — ``Objects_GetObjects`` (``list[ObjectDto]``).
    ``GET /core/api/objects/{objectId}/objectInfo`` — ``Objects_GetObjectInfo``
    (``QuickObjectInfo``).
"""

from datetime import datetime
from uuid import UUID

from pydantic import Field

from ...common.enumerations.objects import ObjectModifyMode
from ..base import IPSModel


class ObjectDto(IPSModel):
    """Полное описание версии информационного объекта.

    Обязательны поля идентичности; остальные объявлены устойчиво к различиям ответов
    (см. практику в [[gotchas]]).

    Внимание (id-пространства): ``object_id`` (=``objectID``=F_OBJECT_ID) — идентификатор
    ОБЪЕКТА, общий для всех его версий; именно его принимают методы ``object_get`` /
    ``objects_collection`` / ``object_info``. ``id`` (=F_ID) — идентификатор версии (записи),
    уникален для каждой версии, и НЕ годится как аргумент ``object_get`` (вернётся ``None``).
    Аналогично парны GUID: ``object_guid`` — объекта, ``guid`` — версии.

    Attributes:
        object_id: Идентификатор ОБЪЕКТА (F_OBJECT_ID), общий для версий; ключ для object_get.
        id: Идентификатор ВЕРСИИ/записи (F_ID), уникален per-версия; ключ для objects_collection.
        version_id: Порядковый номер версии (0 у базовой).
        create_date: Дата создания версии (UTC).
        lc_step: Текущий шаг жизненного цикла (определяет режим правки атрибутов).
        checkout_by: Пользователь, извлёкший версию (checkout); 0 — версия свободна.
        object_type: Идентификатор типа объекта.
        owner_id: Идентификатор владельца.
        creator_id: Идентификатор создателя.
        caption: Заголовок объекта (отображаемое имя).
        name_in_messages: Имя для использования в сообщениях.
        modify_date: Дата последнего изменения (UTC).
        object_ver_type: Тип версии: -1 рабочая копия / 0 обычная / 1 версия web-клиента.
        modification_id: Идентификатор модификации.
        site_id: Идентификатор узла (для распределённых баз).
        is_base_version: Признак базовой (актуальной) версии (F_BASE_VERSION).
        is_creation_mode: Объект в режиме создания (не существует до commitCreation).
        guid: GUID ВЕРСИИ объекта.
        object_guid: GUID ОБЪЕКТА (общий для всех версий); ключ для object_get_by_guid.
        subject_areas: Предметные области объекта.
        parent_version_id: Идентификатор версии-родителя.
        object_modify_mode: Режим правки (inBase/checkout/createVersion/cantModify).
        filtration_state: Состояние фильтрации версии (правила выбора версий).
        project_id: Идентификатор проекта (контекста).
        access_level: Уровень доступа объекта.
        versions_count: Количество версий объекта.
        read_only: Признак доступа только для чтения (правка невозможна).
    """

    object_id: int = Field(
        alias="objectID",
        description=(
            "Идентификатор ОБЪЕКТА (F_OBJECT_ID), общий для всех версий; "
            "ключ для object_get/object_info/object_base_version"
        ),
    )
    id: int = Field(
        description=(
            "Идентификатор ВЕРСИИ/записи (F_ID), уникален per-версия; "
            "ключ для objects_collection, НЕ для object_get"
        )
    )
    version_id: int | None = Field(
        default=None, alias="versionID", description="Порядковый номер версии (0 у базовой)"
    )
    create_date: datetime | None = Field(default=None, description="Дата создания версии (UTC)")
    lc_step: int | None = Field(
        default=None, description="Текущий шаг жизненного цикла (определяет режим правки)"
    )
    checkout_by: int | None = Field(
        default=None, description="Идентификатор пользователя, извлёкшего версию (0 = свободна)"
    )
    object_type: int | None = Field(default=None, description="Идентификатор типа объекта")
    owner_id: int | None = Field(default=None, alias="ownerID", description="Владелец")
    creator_id: int | None = Field(default=None, alias="creatorID", description="Создатель")
    caption: str | None = Field(default=None, description="Заголовок (отображаемое имя) объекта")
    name_in_messages: str | None = Field(
        default=None, description="Имя для использования в сообщениях"
    )
    modify_date: datetime | None = Field(
        default=None, description="Дата последнего изменения (UTC)"
    )
    object_ver_type: int | None = Field(
        default=None,
        description="Тип версии: -1 рабочая копия / 0 обычная / 1 версия web-клиента",
    )
    modification_id: int | None = Field(
        default=None, alias="modificationID", description="Идентификатор модификации"
    )
    site_id: str | None = Field(
        default=None, alias="siteID", description="Идентификатор узла (для распределённых баз)"
    )
    is_base_version: bool | None = Field(
        default=None, description="Признак базовой (актуальной) версии (F_BASE_VERSION)"
    )
    is_creation_mode: bool | None = Field(
        default=None,
        description="Объект в режиме создания (не существует до commitCreation)",
    )
    guid: UUID | None = Field(default=None, description="GUID ВЕРСИИ объекта")
    object_guid: UUID | None = Field(
        default=None,
        alias="objectGUID",
        description="GUID ОБЪЕКТА, общий для версий; ключ для object_get_by_guid",
    )
    subject_areas: str | None = Field(default=None, description="Предметные области объекта")
    parent_version_id: int | None = Field(
        default=None, alias="parentVersionID", description="Идентификатор версии-родителя"
    )
    object_modify_mode: ObjectModifyMode | None = Field(
        default=None,
        description="Режим правки версии (inBase/checkout/createVersion/cantModify)",
    )
    filtration_state: str | None = Field(
        default=None, description="Состояние фильтрации версии (правила выбора версий)"
    )
    project_id: int | None = Field(
        default=None, alias="projectID", description="Идентификатор проекта (контекста)"
    )
    access_level: int | None = Field(default=None, description="Уровень доступа объекта")
    versions_count: int | None = Field(default=None, description="Количество версий объекта")
    read_only: bool | None = Field(
        default=None, description="Только для чтения (правка невозможна)"
    )


class QuickObjectInfo(IPSModel):
    """Краткие сведения об объекте (облегчённая версия для быстрых запросов).

    См. пояснение про id-пространства в :class:`ObjectDto`: ``object_id`` (=``objectID``) —
    идентификатор объекта (F_OBJECT_ID), ``id`` — идентификатор версии (F_ID).

    Attributes:
        id: Идентификатор ВЕРСИИ/записи (F_ID), уникален per-версия.
        object_id: Идентификатор ОБЪЕКТА (F_OBJECT_ID), общий для версий; ключ для object_info.
        object_type_id: Идентификатор типа объекта.
        version_guid: GUID ВЕРСИИ объекта.
        caption: Заголовок (отображаемое имя) объекта.
    """

    id: int = Field(description="Идентификатор ВЕРСИИ/записи (F_ID), уникален per-версия")
    object_id: int = Field(
        alias="objectID",
        description="Идентификатор ОБЪЕКТА (F_OBJECT_ID), общий для версий; ключ для object_info",
    )
    object_type_id: int | None = Field(
        default=None, alias="objectTypeID", description="Идентификатор типа объекта"
    )
    version_guid: UUID | None = Field(default=None, description="GUID ВЕРСИИ объекта")
    caption: str | None = Field(default=None, description="Заголовок (отображаемое имя) объекта")
