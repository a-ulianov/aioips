"""Схема типа связи метаданских IPS.

References:
    ``GET /core/api/metadata/relationTypes`` — массив ``ImsRelationTypeDto``.
"""

from typing import Annotated
from uuid import UUID

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class RelationTypeMeta(IPSModel):
    """Описание типа связи в метаданных IPS.

    Тип связи задаёт семантику ребра между объектами в составе/связях: его прямое
    имя (``type_name``, например «Входит в»), обратное имя (``reverse_name``,
    например «Состоит из») и вид связи (``relation_kind``: 0 — иерархическая,
    1 — неиерархическая). Идентификатор типа связи (``RelationType``) — это
    отдельное id-пространство ТИПОВ связей, не путать с ``RelationID`` конкретной
    связи между объектами (тот нестабилен и не кэшируется).

    Обязательны только поля идентичности (``id``, ``guid``, ``type_name``,
    ``reverse_name``). Прочие поля могут отсутствовать у части типов связей,
    поэтому объявлены с дефолтами — это устойчиво к различиям между типами и
    версиями API.

    Attributes:
        id: Числовой идентификатор типа связи (``RelationType``; принимается
            методами, требующими ``relationTypeId``). По умолчанию в DTO ``-1``.
        guid: Глобальный идентификатор типа связи (переносим между базами).
        description: Отображаемое имя/описание типа связи (например, «Структурная
            связь»).
        type_name: Прямое имя связи (например, «Входит в»).
        reverse_name: Обратное имя связи (например, «Состоит из»).
        check_out_file: Брать ли по этой связи блокировку (checkout) объекта,
            содержащего файлы потомка (1 — берёт, 0 — не берёт).
        relation_kind: Вид связи: 0 — иерархическая (например, состав изделия);
            1 — неиерархическая (ассоциативная).
        area_id: Идентификатор области данных (может отсутствовать).
        any_attributes: Разрешены ли произвольные атрибуты этого типа связи.
        short_name: Краткое имя (может отсутствовать).
        note: Примечание (может отсутствовать).
        options: Набор включённых опций типа связи (``RelationTypeOptions``):
            ``none``/``enableCycleRelations``/``enableCheckAnnulment``.
    """

    id: int = Field(description="RelationType — идентификатор ТИПА связи (не RelationID связи)")
    guid: UUID = Field(description="GUID типа связи (переносим между базами)")
    type_name: str = Field(default="", description="Прямое имя связи (например, «Входит в»)")
    reverse_name: str = Field(default="", description="Обратное имя связи (например, «Состоит из»)")
    description: str = Field(default="", description="Отображаемое имя/описание типа связи")
    check_out_file: int = Field(default=0, description="Брать ли checkout файлов потомка (1/0)")
    relation_kind: int = Field(
        default=0, description="Вид связи: 0 — иерархическая, 1 — неиерархическая"
    )
    area_id: str | None = Field(default=None, description="Идентификатор области данных")
    any_attributes: bool = Field(default=True, description="Разрешены ли произвольные атрибуты")
    short_name: str | None = Field(default=None, description="Краткое имя")
    note: str | None = Field(default=None, description="Примечание")
    options: Annotated[list[str], EmptyListIfNone] = Field(
        default_factory=list, description="Включённые опции типа связи (RelationTypeOptions)"
    )
