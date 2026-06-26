"""Схема определения типа объекта (контроллер ``objectTypes``).

Это определение типа объекта (``ObjectTypeDto``) контроллера ``/core/api/objectTypes``.
Отличается от схемы метамодели ``ImsObjectTypeDto`` раздела ``metadata`` (там — машинное
описание метамодели); здесь — определение типа в составе рабочего контроллера объектов
этого типа.

References:
    ``GET /core/api/objectTypes/{objectTypeId}`` — ``ObjectTypes_GetObjectType``
    (обёртка ``ObjectTypeDtoNullableResultDto`` → ``entity``).
"""

from typing import Annotated
from uuid import UUID

from pydantic import Field

from ...common.enumerations.metadata import InheritMode, ObjectVersionMode
from ..base import EmptyListIfNone, IPSModel


class ObjectTypeDefinition(IPSModel):
    """Определение типа объекта (``ObjectTypeDto`` контроллера ``objectTypes``).

    Описывает один тип объекта: идентичность, режим версионирования, наследование
    схемы ЖЦ, атрибут заголовка, родительский тип и набор опций. В отличие от схемы
    раздела ``metadata`` (``ImsObjectTypeDto`` — машинное описание метамодели), эта
    схема — определение типа в рабочем контроллере ``objectTypes``, рядом с методами
    перечисления реальных объектов (экземпляров) данного типа.

    Внимание (id-пространство): ``object_type`` — идентификатор ТИПА объекта
    (``ObjectTypeID``), общий ключ для всех методов раздела; это НЕ ``ObjectID``/``ID``
    конкретного объекта или его версии. ``parent_type_id`` — тоже ``ObjectTypeID``.

    Обязательно лишь поле идентичности ``object_type``; остальные объявлены устойчиво
    к различиям между типами и версиями API (необязательные с дефолтами).

    Attributes:
        object_type: Идентификатор ТИПА объекта (``ObjectTypeID``); ключ для методов
            раздела. Не путать с ``ObjectID`` конкретного объекта.
        object_type_guid: Глобальный идентификатор типа объекта (переносим между базами).
        object_type_name: Наименование типа объектов (системное).
        object_type_short_name: Краткое наименование типа объектов.
        object_instance_name: Наименование объекта данного типа (например, «Деталь»).
        area_id: Идентификатор предметной области.
        any_attributes: Контроль набора атрибутов; ``false`` — только разрешённые
            атрибуты, ``true`` — допускаются любые.
        public_lc_schema: Наследование схемы ЖЦ (``InheritMode``): ``private``/
            ``public``/``inherited``.
        change_objects_schema: Переводить ли существующие объекты на шаги новой схемы ЖЦ.
        versionable: Режим версионирования (``ObjectVersionMode``): ``abstract``/
            ``singleVersion``/``multiVersion``.
        note: Комментарии.
        default_relation: Идентификатор типа связи по умолчанию для дерева объектов.
        parent_type_id: Идентификатор родительского ТИПА объекта (``ObjectTypeID``).
        caption_attribute: Идентификатор атрибута, формирующего заголовок типа в списках.
        lifetime_reserve: Время жизни удалённых объектов (дни до физического уничтожения).
        options: Набор опций типа объекта (битовые флаги управления свойствами).
        schema_id: Идентификатор схемы ЖЦ для объектов данного типа.
        is_local_type: Является ли тип локальным (только для чтения).
        classified_option: Классификация создаваемых объектов (только для чтения).
    """

    object_type: int = Field(description="ObjectTypeID типа объекта (не ObjectID объекта)")
    object_type_guid: UUID | None = Field(
        default=None, description="GUID типа объекта (переносим между базами)"
    )
    object_type_name: str | None = Field(
        default=None, description="Наименование типа объектов (системное)"
    )
    object_type_short_name: str | None = Field(
        default=None, description="Краткое наименование типа объектов"
    )
    object_instance_name: str | None = Field(
        default=None, description="Наименование объекта данного типа (например, «Деталь»)"
    )
    area_id: str | None = Field(
        default=None, alias="areaID", description="Идентификатор предметной области"
    )
    any_attributes: bool | None = Field(
        default=None, description="Контроль набора атрибутов (true — допускаются любые)"
    )
    public_lc_schema: InheritMode | None = Field(
        default=None,
        alias="publicLCSchema",
        description="Наследование схемы ЖЦ (private/public/inherited)",
    )
    change_objects_schema: bool | None = Field(
        default=None, description="Переводить ли существующие объекты на шаги новой схемы ЖЦ"
    )
    versionable: ObjectVersionMode | None = Field(
        default=None, description="Версионирование (abstract/singleVersion/multiVersion)"
    )
    note: str | None = Field(default=None, description="Комментарии")
    default_relation: int | None = Field(
        default=None, description="Тип связи по умолчанию для дерева объектов"
    )
    parent_type_id: int | None = Field(
        default=None,
        alias="parentTypeID",
        description="Идентификатор родительского типа объекта (ObjectTypeID)",
    )
    caption_attribute: int | None = Field(
        default=None, description="Идентификатор атрибута заголовка типа в списках"
    )
    lifetime_reserve: int | None = Field(
        default=None, description="Время жизни удалённых объектов (дни)"
    )
    options: Annotated[list[str], EmptyListIfNone] = Field(
        default_factory=list, description="Опции типа объекта (битовые флаги свойств)"
    )
    schema_id: int | None = Field(
        default=None, alias="schemaID", description="Идентификатор схемы ЖЦ типа объекта"
    )
    is_local_type: bool | None = Field(
        default=None, description="Является ли тип локальным (только для чтения)"
    )
    classified_option: int | None = Field(
        default=None, description="Классификация создаваемых объектов (только для чтения)"
    )
