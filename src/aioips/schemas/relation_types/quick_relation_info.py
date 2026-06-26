"""Схема краткой информации о связи IPS.

References:
    ``GET /core/api/relationTypes/{relationTypeId}/relations`` — массив
    ``QuickRelationInfoDto``.
"""

from uuid import UUID

from pydantic import Field

from ..base import IPSModel


class QuickRelationInfo(IPSModel):
    """Краткое описание связи между объектами IPS.

    Связь направленная: соединяет объект-родитель (``proj_id`` = ``IDBObject.ObjectID``
    родителя) с версией объекта-потомка (``part_id`` = ``IDBObject.ID`` потомка) в рамках
    типа связи ``relation_type``. Тип связи задаёт смысл отношения родитель→потомок
    (например, состав изделия).

    Внимание: ``relation_id`` нестабилен — он меняется после ``CheckOut``/``CheckIn``
    объекта-родителя, поэтому его нельзя кэшировать. Для устойчивой идентификации связи
    используйте ``guid`` либо тройку (``proj_id``, ``part_id``, ``relation_type``).

    Attributes:
        relation_id: Идентификатор связи (нестабилен, не кэшировать).
        proj_id: Идентификатор объекта-родителя (``IDBObject.ObjectID``).
        part_id: Идентификатор версии объекта-потомка (``IDBObject.ID``).
        relation_type: Идентификатор типа связи.
        guid: Глобальный идентификатор связи (устойчивый ключ).
    """

    relation_id: int | None = Field(
        default=None,
        alias="relationID",
        description="Идентификатор связи (нестабилен, не кэшировать)",
    )
    proj_id: int | None = Field(
        default=None,
        alias="projID",
        description="Идентификатор объекта-родителя (IDBObject.ObjectID)",
    )
    part_id: int | None = Field(
        default=None,
        alias="partID",
        description="Идентификатор версии объекта-потомка (IDBObject.ID)",
    )
    relation_type: int | None = Field(default=None, description="Идентификатор типа связи")
    guid: UUID | None = Field(default=None, description="Глобальный идентификатор связи")
