"""Схемы атрибутов информационного объекта IPS.

Атрибут объекта несёт значение характеристики (обозначение, наименование, масса и т.п.).
Значения атрибута могут быть множественными и иметь разные типы данных (``FieldTypes``),
поэтому ``values`` типизированы как список произвольных JSON-значений. Атрибут-ссылка
(``ftObjectLink``) хранит id объекта-цели (так задаётся связь «документ → Архив»).

Списочные поля могут прийти от IPS как ``null`` вместо ``[]`` — нормализуются валидатором
``EmptyListIfNone`` (см. граблям). Идентификаторы-акронимы (``attributeID`` и др.)
имеют явные алиасы под точный ключ JSON. См. объектной модели IPS (раздел «Атрибуты»).

References:
    ``GET /core/api/objects/{objectId}/attributes`` — ``ObjectAttributes_GetAttributes``.
    ``GET /core/api/objects/{objectId}/attributesValues`` — ``ObjectAttributes_GetAttributesValues``
"""

from typing import Annotated, Any
from uuid import UUID

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class Attribute(IPSModel):
    """Атрибут объекта вместе со значением и метаданными.

    Внимание: ключи JSON этого DTO используют заглавные суффиксы (``attributeID``,
    ``dbObjectID``, ``dB_ID``) — для них заданы явные алиасы (см. граблям).

    Атрибут-ссылка (``ftObjectLink``/``ftObjectLinkByID``) хранит id объекта-цели — так
    устроена, например, привязка «документ → Архив». Множественный атрибут несёт
    несколько значений (``values_count`` > 1).

    Attributes:
        name: Имя атрибута.
        attribute_id: Идентификатор ТИПА атрибута (какая характеристика).
        db_object_id: Идентификатор объекта в БД.
        db_id: Внутренний идентификатор записи значения в БД.
        is_null: Признак отсутствия значения.
        as_string: Строковое представление значения.
        values_count: Количество значений (для множественных атрибутов).
        index: Порядковый индекс значения.
        data_type: Тип данных атрибута (``FieldTypes``, напр. ``ftString``/``ftObjectLink``).
        is_system: Признак системного атрибута.
        values: Список значений (типы зависят от ``data_type``; для ``ftObjectLink`` — id цели).
        description: Описание значения.
        descriptions: Описания для множественных значений.
        read_only: Признак доступа только для чтения.
        group_name: Имя группы атрибутов.
        visible: Признак видимости атрибута.
        attribute_type_info: Сведения о типе атрибута (метаданные), как есть.
    """

    name: str | None = Field(default=None, description="Имя атрибута")
    attribute_id: int = Field(
        alias="attributeID", description="Идентификатор ТИПА атрибута (какая характеристика)"
    )
    db_object_id: int | None = Field(
        default=None, alias="dbObjectID", description="Идентификатор объекта в БД"
    )
    db_id: int | None = Field(
        default=None, alias="dB_ID", description="Внутренний идентификатор записи значения в БД"
    )
    is_null: bool | None = Field(default=None, description="Признак отсутствия значения")
    as_string: str | None = Field(default=None, description="Строковое представление значения")
    values_count: int | None = Field(
        default=None, description="Количество значений (для множественных атрибутов)"
    )
    index: int | None = Field(default=None, description="Порядковый индекс значения")
    data_type: str | None = Field(
        default=None,
        description="Тип данных атрибута (FieldTypes: ftString/ftInteger/ftObjectLink/ftFile/…)",
    )
    is_system: bool | None = Field(default=None, description="Признак системного атрибута")
    values: Annotated[list[Any], EmptyListIfNone] = Field(
        default_factory=list,
        description="Значения (типы зависят от data_type; для ftObjectLink — id объекта-цели)",
    )
    description: str | None = Field(default=None, description="Описание значения")
    descriptions: Annotated[list[str], EmptyListIfNone] = Field(
        default_factory=list, description="Описания для множественных значений"
    )
    read_only: bool | None = Field(
        default=None, description="Только для чтения (правка значения невозможна)"
    )
    group_name: str | None = Field(default=None, description="Имя группы атрибутов")
    visible: bool | None = Field(default=None, description="Признак видимости атрибута")
    attribute_type_info: dict[str, Any] | None = Field(
        default=None, description="Сведения о типе атрибута (метаданные), как есть"
    )


class AttributeValues(IPSModel):
    """Значения атрибута объекта с расширенными метаданными типа и режимов.

    Возвращается методом ``object_attributes_values``. По сравнению с :class:`Attribute`
    дополнительно несёт GUID и псевдоним атрибута, режим множественности
    (``MultiValueModes``) и режим вычисления (``ComputeValueModes``), а также извлечённые
    (разрешённые) значения.

    Attributes:
        attribute_id: Идентификатор ТИПА атрибута.
        attribute_name: Имя атрибута.
        attribute_guid: GUID типа атрибута.
        attribute_alias: Псевдоним (alias) атрибута.
        attribute_type: Тип данных атрибута (``FieldTypes``).
        values: Список значений (для ``ftObjectLink`` — id объекта-цели).
        extracted_values: Извлечённые (разрешённые) значения.
        descriptions: Описания значений.
        multiple_valued: Режим множественности значений (``MultiValueModes``).
        compute_mode: Режим вычисления значений (``ComputeValueModes``).
        read_only: Признак доступа только для чтения.
        group_name: Имя группы атрибутов.
        is_new: Признак нового (несохранённого) значения.
        is_force_delete: Признак принудительного удаления.
        throw_set_exception: Признак генерации исключения при установке.
        attribute_type_info: Сведения о типе атрибута (метаданные), как есть.
    """

    attribute_id: int = Field(description="Идентификатор ТИПА атрибута")
    attribute_name: str | None = Field(default=None, description="Имя атрибута")
    attribute_guid: UUID | None = Field(default=None, description="GUID типа атрибута")
    attribute_alias: str | None = Field(default=None, description="Псевдоним (alias) атрибута")
    attribute_type: str | None = Field(default=None, description="Тип данных атрибута (FieldTypes)")
    values: Annotated[list[Any], EmptyListIfNone] = Field(
        default_factory=list,
        description="Значения (типы зависят от attribute_type; для ftObjectLink — id цели)",
    )
    extracted_values: Annotated[list[Any], EmptyListIfNone] = Field(
        default_factory=list,
        description="Извлечённые (разрешённые) значения, напр. для атрибутов из списка",
    )
    descriptions: Annotated[list[Any], EmptyListIfNone] = Field(
        default_factory=list, description="Описания значений"
    )
    multiple_valued: str | None = Field(
        default=None, description="Режим множественности значений (MultiValueModes)"
    )
    compute_mode: str | None = Field(
        default=None, description="Режим вычисления значений (ComputeValueModes)"
    )
    read_only: bool | None = Field(default=None, description="Только для чтения")
    group_name: str | None = Field(default=None, description="Имя группы атрибутов")
    is_new: bool | None = Field(
        default=None, description="Признак нового (несохранённого) значения"
    )
    is_force_delete: bool | None = Field(
        default=None, description="Признак принудительного удаления"
    )
    throw_set_exception: bool | None = Field(
        default=None, description="Признак генерации исключения при установке значения"
    )
    attribute_type_info: dict[str, Any] | None = Field(
        default=None, description="Сведения о типе атрибута (метаданные), как есть"
    )
