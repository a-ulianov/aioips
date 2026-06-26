"""Схемы связи между информационными объектами IPS.

Связь (``IDBRelation``) — направленное отношение «родитель → потомок» в составе изделия.
Родитель задаётся ``ProjID`` (это ``ObjectID`` объекта-родителя, общий для всех его версий),
потомок — ``PartID`` (это ``ID`` конкретной версии объекта-потомка). Дополнительно может
указываться ``PartObjectID`` (``ObjectID`` потомка, ``0`` если связь не привязана к версии).

Внимание: IPS сериализует имена .NET-свойств с заглавными суффиксами-акронимами
(``relationID``, ``projID``, ``partID``, ``partObjectID``). ``to_camel`` не воспроизводит такое
написание, поэтому для этих полей заданы явные алиасы, равные точному ключу JSON (см. [[gotchas]]).

Предупреждение: ``RelationID`` нестабилен — он меняется после ``CheckOut``/``CheckIn``
родителя, поэтому кэшировать его нельзя. Устойчивый ключ связи — её ``GUID`` либо тройка
(``ProjID``, ``PartID``, ``RelationType``).

References:
    ``GET /core/api/relations/{relationId}`` — ``Relations_GetRelation`` (``RelationDto``).
    ``GET /core/api/Relations/GetRelationTypes`` — ``RelationTypeDTO``.
"""

from datetime import datetime
from uuid import UUID

from pydantic import Field

from ..base import IPSModel


class Relation(IPSModel):
    """Связь между объектом-родителем и версией объекта-потомка.

    Связь направленная: родитель (``proj_id`` = ``ObjectID`` родителя) → потомок
    (``part_id`` = ``ID`` версии потомка). Идентификатор связи (``relation_id``) нестабилен
    и не должен кэшироваться; для устойчивой идентификации используйте ``guid`` или тройку
    (``proj_id``, ``part_id``, ``relation_type``).

    Attributes:
        relation_id: Идентификатор связи (нестабилен — меняется при checkout/checkin).
        proj_id: Идентификатор объекта-родителя (``IDBObject.ObjectID``).
        part_object_id: Идентификатор объекта-потомка (``IDBObject.ObjectID``); ``0``, если
            связь не привязана к конкретной версии потомка.
        part_id: Идентификатор версии объекта-потомка (``IDBObject.ID``).
        relation_type: Идентификатор типа связи.
        creator_id: Идентификатор создателя связи.
        create_date: Дата создания связи (UTC); ``DateTime.MinValue`` трактуется как отсутствие.
        filtration_owner_id: Идентификатор узла, по которому строятся правила выбора версий.
        guid: Глобальный идентификатор связи (устойчивый ключ).
        read_only: Признак того, что связь доступна только для чтения.
    """

    relation_id: int = Field(alias="relationID", description="Идентификатор связи (нестабилен)")
    proj_id: int = Field(alias="projID", description="ObjectID объекта-родителя")
    part_id: int = Field(alias="partID", description="ID версии объекта-потомка")
    relation_type: int = Field(description="Идентификатор типа связи")
    part_object_id: int | None = Field(
        default=None,
        alias="partObjectID",
        description="ObjectID объекта-потомка (0 — не по версии)",
    )
    creator_id: int | None = Field(
        default=None, alias="creatorID", description="Идентификатор создателя связи"
    )
    create_date: datetime | None = Field(default=None, description="Дата создания связи (UTC)")
    filtration_owner_id: str | None = Field(
        default=None, alias="filtrationOwnerID", description="Узел правил выбора версий"
    )
    guid: UUID | None = Field(default=None, description="Глобальный идентификатор связи")
    read_only: bool | None = Field(default=None, description="Только для чтения")


class RelationType(IPSModel):
    """Описание типа связи между информационными объектами.

    Тип связи определяет семантику отношения родитель → потомок. У типа есть прямое имя
    (``name``) и обратное (``reverse_name``), описывающее отношение со стороны потомка.

    Attributes:
        id: Идентификатор типа связи.
        guid: Глобальный идентификатор типа связи.
        description: Описание типа связи.
        name: Наименование связи (прямое, со стороны родителя).
        reverse_name: Обратное наименование связи (со стороны потомка).
        note: Примечание к типу связи.
    """

    id: int = Field(description="Идентификатор типа связи")
    guid: UUID | None = Field(default=None, description="Глобальный идентификатор типа связи")
    description: str | None = Field(default=None, description="Описание типа связи")
    name: str | None = Field(default=None, description="Наименование связи (прямое)")
    reverse_name: str | None = Field(
        default=None, description="Обратное наименование связи (со стороны потомка)"
    )
    note: str | None = Field(default=None, description="Примечание")
