"""Схема поисковой схемы (выборки) IPS и её дополнительных колонок.

References:
    ``GET /core/api/searchSchemes/{objectId}/getById`` — ``SearchSchemaDto``.
"""

from enum import StrEnum
from typing import Annotated

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class AttributeSourceType(StrEnum):
    """Источник значения атрибута для колонки поисковой схемы (``AttributeSourceTypes``).

    Определяет, откуда берётся значение атрибута, выводимого в колонке результата
    поиска. Соответствует строковому enum ``AttributeSourceTypes`` IPS Web API.

    Attributes:
        AUTO: Источник определяется автоматически.
        OBJECT: Атрибут объекта.
        RELATION: Атрибут связи.
        EVENTS: Атрибут события.
        HISTORY: Атрибут истории объекта.
        FILE_STORAGE: Атрибут файлового хранилища.
        SNAPSHOT: Атрибут снимка.
        OTHER: Прочий источник.
    """

    AUTO = "auto"
    OBJECT = "object"
    RELATION = "relation"
    EVENTS = "events"
    HISTORY = "history"
    FILE_STORAGE = "fileStorage"
    SNAPSHOT = "snapshot"
    OTHER = "other"


class SearchSchemaAdditionalColumn(IPSModel):
    """Дополнительная колонка поисковой схемы (``SearchSchemaAdditionalColumnDto``).

    Описывает один атрибут, выводимый отдельной колонкой в результатах поиска по
    схеме: какой атрибут (``attribute``), откуда брать его значение (``source``) и
    какой ширины колонка (``width``).

    Attributes:
        attribute: Идентификатор атрибута, отображаемого в колонке.
        source: Источник значения атрибута (см. :class:`AttributeSourceType`).
        width: Ширина колонки в пикселях (если задана).
    """

    attribute: int = Field(description="Идентификатор атрибута колонки")
    source: AttributeSourceType = Field(description="Источник значения атрибута")
    width: int | None = Field(default=None, description="Ширина колонки в пикселях")


class SearchScheme(IPSModel):
    """Сохранённая поисковая схема (выборка) IPS (``SearchSchemaDto``).

    Поисковая схема — это именованная конфигурация поиска объектов: направление
    обхода, правило версий, типы искомых объектов, набор выводимых колонок и
    привязка к ролям. По схеме строится фактический поиск/выборка объектов; её
    структуру условий описывает :meth:`condition_structure_info`.

    Все поля, кроме служебных флагов и идентификаторов выборки, необязательны:
    списки приходят ``null`` для пустых наборов и приводятся к ``[]``. Это делает
    модель устойчивой к различиям между схемами и версиями API.

    Attributes:
        search_schema_name: Наименование поисковой схемы (выборки).
        personal: Признак персональной (личной) схемы, а не общей.
        search_direction: Направление поиска по связям (числовой код).
        group_by_versions: Группировать результаты по версиям объекта.
        only_actual_versions: Учитывать только актуальные версии объектов.
        selector: Идентификатор селектора (выборки), к которому привязана схема.
        version_rule: Правило отбора версий (``VersionsRule``) для поиска.
        include_in_production_selector: Включать схему в производственный селектор.
        searched_object_types: Типы объектов, среди которых ведётся поиск.
        expand_composition_object_types: Типы объектов, чей состав раскрывается.
        dont_expand_composition_object_types: Типы объектов, чей состав не раскрывается.
        relation_types: Типы связей, по которым выполняется обход.
        columns: Дополнительные колонки результата (см. :class:`SearchSchemaAdditionalColumn`).
        roles: Идентификаторы ролей, которым доступна схема.
    """

    search_schema_name: str | None = Field(default=None, description="Наименование поисковой схемы")
    personal: bool = Field(default=False, description="Персональная (личная) схема")
    search_direction: int | None = Field(default=None, description="Направление поиска по связям")
    group_by_versions: bool = Field(default=False, description="Группировать по версиям объекта")
    only_actual_versions: bool = Field(
        default=False, description="Только актуальные версии объектов"
    )
    selector: int | None = Field(default=None, description="Идентификатор селектора (выборки)")
    version_rule: int | None = Field(default=None, description="Правило отбора версий")
    include_in_production_selector: bool = Field(
        default=False, description="Включать в производственный селектор"
    )
    searched_object_types: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list, description="Типы искомых объектов"
    )
    expand_composition_object_types: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list, description="Типы объектов с раскрытием состава"
    )
    dont_expand_composition_object_types: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list, description="Типы объектов без раскрытия состава"
    )
    relation_types: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list, description="Типы связей для обхода"
    )
    columns: Annotated[list[SearchSchemaAdditionalColumn], EmptyListIfNone] = Field(
        default_factory=list, description="Дополнительные колонки результата"
    )
    roles: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list, description="Идентификаторы ролей с доступом к схеме"
    )
