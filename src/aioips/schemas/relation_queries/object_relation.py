"""Схема записи состава/вхождения объекта IPS.

References:
    ``GET /core/api/Relations/ConsistFrom`` и
    ``GET /core/api/Relations/EntersInVersion`` — массив ``ObjectRelationDTO``.
"""

from uuid import UUID

from pydantic import Field

from ..base import IPSModel


class ObjectRelation(IPSModel):
    """Одна связь состава/вхождения между двумя объектами IPS.

    Описывает ребро графа связей: родитель (``parent_object_id``) → потомок
    (``object_id``) с типом связи ``relation_type_id``. Возвращается методами
    :meth:`~aioips.IPSClient.consist_from` (из чего состоит объект) и
    :meth:`~aioips.IPSClient.enters_in_version` (куда объект входит). Все
    идентификаторы здесь — это ``objectID`` (F_OBJECT_ID, общий для версий),
    а не ``id`` версии; ``part_id`` дополнительно адресует конкретную версию
    потомка в составе.

    Этот тип относится к разделу запросов состава (``/core/api/Relations/...``)
    и НЕ совпадает со схемой связи раздела ``relations`` (строчная ``r``),
    описывающего отдельную запись связи и её жизненный цикл.

    Attributes:
        relation_type_id: Идентификатор типа связи (см. :class:`RelationTypeBrief`).
        parent_object_id: Идентификатор ОБЪЕКТА-родителя (``objectID``).
        parent_object_type_id: Идентификатор типа объекта-родителя.
        object_id: Идентификатор ОБЪЕКТА-потомка (``objectID``).
        object_guid: Глобальный идентификатор объекта-потомка (объект, не версия).
        object_type_id: Идентификатор типа объекта-потомка.
        part_id: Идентификатор версии потомка в составе (``partID`` / F_ID).
    """

    relation_type_id: int = Field(default=0, description="Идентификатор типа связи")
    parent_object_id: int = Field(default=0, description="Идентификатор объекта-родителя")
    parent_object_type_id: int = Field(default=0, description="Идентификатор типа объекта-родителя")
    object_id: int = Field(default=0, description="Идентификатор объекта-потомка (objectID)")
    object_guid: UUID | None = Field(
        default=None, description="Глобальный идентификатор объекта-потомка"
    )
    object_type_id: int = Field(default=0, description="Идентификатор типа объекта-потомка")
    part_id: int = Field(default=0, description="Идентификатор версии потомка в составе (partID)")
