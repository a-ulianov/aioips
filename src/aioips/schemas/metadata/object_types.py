"""Схема типа объекта метаданных IPS.

References:
    ``GET /core/api/metadata/objectTypes`` — массив ``ImsObjectTypeDto``.
"""

from typing import Annotated
from uuid import UUID

from pydantic import Field

from ...common.enumerations.metadata import (
    InheritMode,
    ObjectsClassifyType,
    ObjectVersionMode,
)
from ..base import EmptyListIfNone, IPSModel


class ObjectType(IPSModel):
    """Описание типа объекта в метаданных IPS.

    Обязательны только поля идентичности (``id``, ``guid``, имена). Остальные поля
    в реальных ответах присутствуют не у всех типов объектов, поэтому объявлены
    необязательными — это устойчиво к различиям между типами и версиями API.

    Attributes:
        id: Числовой идентификатор типа объекта (``ObjectTypeID``; принимается методами,
            требующими ``objectTypeId``). Это id-пространство ТИПОВ, не ``ObjectID`` объекта.
        guid: Глобальный идентификатор типа объекта (переносим между базами).
        object_type_name: Системное имя типа объекта.
        object_name: Отображаемое имя типа объекта.
        versions_mode: Режим версионирования (``ObjectVersionMode``): ``abstract``/
            ``singleVersion``/``multiVersion``.
        default_relation: Идентификатор типа связи по умолчанию (``RelationType``).
        area_id: Идентификатор области данных.
        scheme_id: Идентификатор схемы.
        public_life_cycle_scheme: Режим наследования схемы ЖЦ (``InheritMode``):
            ``private``/``public``/``inherited``.
        lifetime_reserve: Резерв времени жизни.
        caption_attribute_id: Идентификатор атрибута, формирующего заголовок объекта
            (id из пространства типов атрибутов).
        any_attributes: Разрешены ли произвольные атрибуты.
        short_name: Краткое имя.
        note: Примечание.
        classify_type: Тип классификации (``ObjectsClassifyType``): ``none``/
            ``selective``/``obligatory``.
        options: Набор включённых опций типа объекта.
    """

    id: int = Field(description="ObjectTypeID типа объекта (не ObjectID конкретного объекта)")
    guid: UUID = Field(description="GUID типа объекта (переносим между базами)")
    object_type_name: str = Field(description="Системное имя типа объекта")
    object_name: str = Field(description="Отображаемое имя типа объекта")
    versions_mode: ObjectVersionMode | None = Field(
        default=None, description="Версионирование (ObjectVersionMode): single/multiVersion"
    )
    default_relation: int | None = Field(default=None, description="Тип связи по умолчанию")
    area_id: str | None = Field(default=None, description="Идентификатор области данных")
    scheme_id: int | None = Field(default=None, description="Идентификатор схемы")
    public_life_cycle_scheme: InheritMode | None = Field(
        default=None, description="Режим наследования схемы жизненного цикла"
    )
    lifetime_reserve: int | None = Field(default=None, description="Резерв времени жизни")
    caption_attribute_id: int | None = Field(
        default=None, description="Идентификатор атрибута заголовка"
    )
    any_attributes: bool | None = Field(
        default=None, description="Разрешены ли произвольные атрибуты"
    )
    short_name: str | None = Field(default=None, description="Краткое имя")
    note: str | None = Field(default=None, description="Примечание")
    classify_type: ObjectsClassifyType | None = Field(
        default=None, description="Тип классификации объектов"
    )
    options: Annotated[list[str], EmptyListIfNone] = Field(
        default_factory=list, description="Включённые опции типа объекта"
    )
