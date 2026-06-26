"""Схема краткого описания типа связи IPS.

References:
    ``GET /core/api/Relations/GetRelationTypes`` — массив ``RelationTypeDTO``.
"""

from uuid import UUID

from pydantic import Field

from ..base import IPSModel


class RelationTypeBrief(IPSModel):
    """Краткое описание типа связи (справочник типов связей IPS).

    Тип связи задаёт семантику ребра состава/вхождения: его идентификатор
    встречается в поле ``relation_type_id`` записей :class:`ObjectRelation`.
    Поле ``name`` — наименование связи в прямом направлении (родитель → потомок),
    ``reverse_name`` — в обратном (потомок → родитель). Возвращается методом
    :meth:`~aioips.IPSClient.relation_queries_relation_types`.

    Имя класса — ``RelationTypeBrief`` (а не ``RelationType``), чтобы не
    конфликтовать со схемами раздела ``relations`` (строчная ``r``), который
    оперирует отдельной записью связи и её жизненным циклом.

    Attributes:
        id: Числовой идентификатор типа связи (обязателен).
        guid: Глобальный идентификатор типа связи.
        description: Описание типа связи.
        name: Наименование связи в прямом направлении (родитель → потомок).
        reverse_name: Наименование связи в обратном направлении (потомок → родитель).
        note: Примечание к типу связи.
    """

    id: int = Field(description="Идентификатор типа связи")
    guid: UUID | None = Field(default=None, description="Глобальный идентификатор типа связи")
    description: str | None = Field(default=None, description="Описание типа связи")
    name: str | None = Field(default=None, description="Наименование связи (прямое направление)")
    reverse_name: str | None = Field(
        default=None, description="Наименование связи (обратное направление)"
    )
    note: str | None = Field(default=None, description="Примечание к типу связи")
