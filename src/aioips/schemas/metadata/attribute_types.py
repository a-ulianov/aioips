"""Схема типа атрибута метаданных IPS.

Тип атрибута описывает характеристику, которую могут нести объекты: его тип данных
(``FieldTypes``: строка, число, дата, ссылка на объект, файл и т.д.), режим
множественности значений, режим вычисляемости и прочие настройки. Сами значения
атрибутов хранятся в объектах; тип атрибута — это их метаописание (см.
объектной модели IPS).

Внимание: IPS сериализует имена .NET-свойств с заглавными суффиксами-акронимами
(``masterAttributeId`` приходит как ``masterAttributeId``, но идентификаторы вида
``...ID`` встречаются и в верхнем регистре). Для устойчивости к различиям casing'а
поля с суффиксом-идентификатором снабжены явными алиасами, равными точному ключу JSON.

References:
    ``GET /core/api/metadata/attributeTypes`` — массив ``ImsAttributeTypeDto``.
    ``GET /core/api/metadata/attributeTypes/{id}`` — ``ImsAttributeTypeDtoNullableResultDto``.
    ``GET /core/api/metadata/attributeTypes/byGuid/{guid}`` — то же (NullableResult).
"""

from typing import Annotated, Any
from uuid import UUID

from pydantic import Field

from ...common.enumerations.attribute import (
    ComputeValueMode,
    FieldType,
    MultiValueMode,
)
from ..base import EmptyListIfNone, IPSModel


class AttributeType(IPSModel):
    """Описание типа атрибута в метаданных IPS.

    Обязательны только поля идентичности (``id``, ``guid``, ``name``). Остальные поля
    в реальных ответах присутствуют не у всех типов атрибутов, поэтому объявлены
    необязательными — это устойчиво к различиям между типами и версиями API.

    Attributes:
        id: Числовой идентификатор типа атрибута.
        guid: Глобальный идентификатор типа атрибута.
        name: Имя атрибута.
        short_name: Короткое имя атрибута.
        alias: Альтернативное имя атрибута (для удобства обращения по строке).
        note: Примечание.
        field_type: Тип данных атрибута (``FieldType``): ``ftString``/``ftInteger``/
            ``ftDouble``/``ftDateTime`` (UTC)/``ftFile``/``ftObjectLink``(ссылка =
            id объекта-цели)/``ftMeasured`` (величина+ед.изм.)/``ftBoolean``/``ftMemo``/
            ``ftBlob``/``ftGuid``/``ftSystem`` и др. (18 значений).
        real_field_type: Реальный тип данных, если ``field_type == ftSystem``.
        default_value: Значение по умолчанию (тип зависит от ``field_type``).
        multi_value_mode: Режим множественности (``MultiValueMode``): ``singleValue``/
            ``multiValues``/``singleValueFromList``/``multiValuesFromList`` (у
            ``…FromList`` значения ограничены ``possible_values``).
        computed: Режим вычисляемости (``ComputeValueMode``): ``notComputableValue``/
            ``storedValue``/``jitValue``/``indexValue``.
        size_type: Размерный параметр атрибута (трактовка зависит от типа данных).
        formula: Формула вычисления значения для вычисляемых атрибутов.
        unique: Режим контроля уникальности значения атрибута.
        level_id: Идентификатор уровня доступности.
        language_id: Идентификатор языка.
        area_id: Идентификатор предметной области.
        optimization_mode: Режим оптимизации хранения значений атрибута.
        is_content: Является ли атрибут содержимым объекта (составным значением).
        options: Набор флагов-опций атрибута.
        mask: Маска ввода значений атрибута.
        master_attribute_id: Идентификатор мастер-атрибута для атрибута-ссылки.
        source_attribute_id: Идентификатор атрибута-источника значения мастер-атрибута.
        value_field_name: Имя поля БД для хранения значения атрибута.
        text_field_name: Имя поля БД для хранения текстового представления значения.
        possible_value_field_name: Имя поля БД для хранения возможных значений.
        field_names: Список имён полей для атрибутов со сложным составным значением.
        possible_values: Список возможных значений атрибута.
        possible_values_descriptions: Описания возможных значений атрибута.
    """

    id: int = Field(description="Идентификатор типа атрибута (id-пространство типов атрибутов)")
    guid: UUID = Field(description="GUID типа атрибута (переносим между базами)")
    name: str = Field(description="Имя атрибута (ключ для attribute_type_id_by_name)")
    short_name: str | None = Field(default=None, description="Короткое имя атрибута")
    alias: str | None = Field(default=None, description="Альтернативное имя атрибута")
    note: str | None = Field(default=None, description="Примечание")
    field_type: FieldType | None = Field(
        default=None, description="Тип данных (FieldType): ftString/ftInteger/ftObjectLink/…"
    )
    real_field_type: FieldType | None = Field(
        default=None, description="Реальный тип данных (если field_type == ftSystem)"
    )
    default_value: Any | None = Field(default=None, description="Значение по умолчанию")
    multi_value_mode: MultiValueMode | None = Field(
        default=None, description="Множественность (MultiValueMode): singleValue/multiValues/…"
    )
    computed: ComputeValueMode | None = Field(
        default=None, description="Вычисляемость (ComputeValueMode): storedValue/jitValue/…"
    )
    size_type: int | None = Field(default=None, description="Размерный параметр атрибута")
    formula: str | None = Field(default=None, description="Формула вычисления значения")
    unique: str | None = Field(default=None, description="Режим контроля уникальности значения")
    level_id: int | None = Field(default=None, description="Уровень доступности")
    language_id: str | None = Field(default=None, description="Идентификатор языка")
    area_id: str | None = Field(default=None, description="Предметная область")
    optimization_mode: str | None = Field(default=None, description="Режим оптимизации хранения")
    is_content: bool | None = Field(default=None, description="Является ли атрибут содержимым")
    options: Annotated[list[str], EmptyListIfNone] = Field(
        default_factory=list, description="Набор флагов-опций атрибута"
    )
    mask: str | None = Field(default=None, description="Маска ввода значений")
    master_attribute_id: int | None = Field(
        default=None, description="Идентификатор мастер-атрибута"
    )
    source_attribute_id: int | None = Field(
        default=None, description="Идентификатор атрибута-источника"
    )
    value_field_name: str | None = Field(default=None, description="Имя поля БД для значения")
    text_field_name: str | None = Field(
        default=None, description="Имя поля БД для текстового представления"
    )
    possible_value_field_name: str | None = Field(
        default=None, description="Имя поля БД для возможных значений"
    )
    field_names: Annotated[list[str], EmptyListIfNone] = Field(
        default_factory=list, description="Имена полей составного значения"
    )
    possible_values: Annotated[list[Any], EmptyListIfNone] = Field(
        default_factory=list, description="Список возможных значений"
    )
    possible_values_descriptions: Annotated[list[Any], EmptyListIfNone] = Field(
        default_factory=list, description="Описания возможных значений"
    )
