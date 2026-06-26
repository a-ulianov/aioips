"""Схемы расширенного (параметризованного) поиска связей IPS.

В отличие от скалярных запросов состава (``relation_queries``: ``consist_from`` /
``enters_in_version``), которые дают быстрый обзор «из чего состоит / куда входит»
по id объекта, эти схемы описывают ПОЛНЫЙ параметризованный поиск связей: с условиями
(:class:`SelectCondition`), отбором атрибутов связи, контекстом версий и (для
:class:`RelationsSelectParameters`) сортировкой и keyset-пагинацией.

Результат поиска — список :class:`RelationSelectResult` (id связи + значения
запрошенных атрибутов связи), а не объекты-потомки.

References:
    ``POST /core/api/relations/consistFrom`` — ``Relations_ExtendedConsistFrom``.
    ``POST /core/api/relations/entersIn`` — ``Relations_ExtendedEntersIn``.
    ``POST /core/api/relations/entersInVersion`` — ``Relations_ExtendedEntersInVersion``.
    ``POST /core/api/relations/select`` — ``Relations_GetSelectsRelations``.
    DTO: ``ObjectRelationsSelectParametersDto``, ``RelationsSelectParametersDto``,
    ``RelationSelectResultDto``, ``AttributeResultDto``.
"""

from datetime import datetime
from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class ObjectRelationsSelectParameters(IPSModel):
    """Параметры расширенного поиска связей конкретного объекта.

    Тело запросов ``consist_from`` / ``enters_in`` / ``enters_in_version``: задаёт объект
    (``object_id``), тип искомых связей и набор условий/атрибутов. В отличие от скалярных
    ``relation_queries.consist_from`` / ``enters_in_version`` (быстрый обзор по id объекта),
    здесь поиск управляем: фильтрация по типам объектов-потомков, произвольные условия,
    отбор конкретных атрибутов связи, контекст версий и срез на дату.

    Предусловие по id-пространству: ``object_id`` — идентификатор ОБЪЕКТА
    (``objectID`` / F_OBJECT_ID), общий для всех версий, а НЕ идентификатор версии
    (``id`` / F_ID). См. объектной модели IPS (раздел «Связи»).

    Крупные/вложенные структуры (``attributes_to_select``, ``conditions``, ``context_rule``)
    типизированы как ``list[Any]`` / ``dict[str, Any]``: их форма (``AttributesToSelectDto``,
    ``SelectConditionDto``, ``ContextRuleDto``) объёмна и устойчива, поэтому передаётся как
    «сырые» JSON-совместимые структуры без отдельных схем — это сохраняет гибкость
    параметризации и не дублирует доменные перечисления.

    Attributes:
        object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), чьи связи ищутся.
        relation_type_id: Идентификатор типа связи (``-1`` — связи любого типа).
        attributes_to_select: Атрибуты связи, значения которых вернуть для каждой связи
            (элементы по форме ``AttributesToSelectDto``: ``attributeId`` + ``source`` +
            ``contents``). Обязателен (может быть пустым списком).
        object_type_id: Идентификатор типа объекта (``-1`` — объекты любого типа).
        child_object_types: Идентификаторы типов объектов-потомков; уточняет ``object_type_id``
            (для каждого типа связи можно указать свои допустимые типы потомков).
        conditions: Условия поиска (элементы по форме ``SelectConditionDto``).
        recursive: Если ``True`` — поиск ведётся по всему дереву состава (все уровни).
        actual_date_time: Дата среза, на которую строится поиск (UTC).
        local_types_mode: Режим локальных типов объектов; результат содержит только
            предопределённые атрибуты (``F_GUID``, ``CAPTION``) без пользовательских.
        context_rule: Дополнительные параметры контекста версий (форма ``ContextRuleDto``).
    """

    object_id: int = Field(description="Идентификатор ОБЪЕКТА (objectID / F_OBJECT_ID)")
    relation_type_id: int = Field(description="Идентификатор типа связи (-1 — любой)")
    attributes_to_select: list[Any] = Field(
        default_factory=list,
        description="Атрибуты связи для отбора (форма AttributesToSelectDto)",
    )
    object_type_id: int | None = Field(
        default=None, description="Идентификатор типа объекта (-1 — любой)"
    )
    child_object_types: list[int] | None = Field(
        default=None, description="Идентификаторы типов объектов-потомков"
    )
    conditions: list[Any] | None = Field(
        default=None, description="Условия поиска (форма SelectConditionDto)"
    )
    recursive: bool | None = Field(
        default=None, description="Рекурсивный обход всего дерева состава"
    )
    actual_date_time: datetime | None = Field(default=None, description="Дата среза поиска (UTC)")
    local_types_mode: bool | None = Field(
        default=None, description="Режим локальных типов объектов"
    )
    context_rule: dict[str, Any] | None = Field(
        default=None, description="Параметры контекста версий (форма ContextRuleDto)"
    )


class RelationsSelectParameters(IPSModel):
    """Параметры произвольной выборки связей (без привязки к одному объекту).

    Тело запроса ``relations_select``: ищет связи по типу, условиям и атрибутам в целом по
    базе (не от конкретного ``object_id``), с сортировкой и keyset-пагинацией. Применять,
    когда нужно перечислить/отфильтровать связи заданного типа массово, а не получить состав
    одного объекта (для этого — :class:`ObjectRelationsSelectParameters`).

    Пагинация keyset (не offset): продолжение страницы задаётся ``last_key_value`` и
    ``last_order_value`` из предыдущего ответа; для устойчивости фиксируйте ``sort_columns``,
    ``orders`` и ``sort_sources``.

    Крупные/вложенные структуры (``attribute_content_overrides``, ``orders``, ``sort_sources``,
    ``conditions``, ``context_rule``, ``last_order_value``) типизированы как ``list[Any]`` /
    ``dict[str, Any]``: они опираются на доменные перечисления (``SortOrders``,
    ``AttributeSourceTypes``, ``ColumnContents``) и устойчивые DTO, поэтому передаются как
    «сырые» JSON-совместимые структуры без отдельных схем.

    Attributes:
        relation_type_id: Идентификатор типа связи (``-1`` — связи любого типа).
        attribute_ids_to_select: Идентификаторы атрибутов связи, значения которых вернуть.
            Обязателен (может быть пустым списком).
        object_type_id: Идентификатор типа объекта (``-1`` — объекты любого типа).
        child_object_types: Идентификаторы типов объектов-потомков; уточняет ``object_type_id``.
        attribute_content_overrides: Переопределение содержимого колонок-атрибутов (форма
            ``AttributeOverrideContentDto``); по умолчанию используется ``ColumnContents.Text``.
        sort_columns: Идентификаторы атрибутов, по которым сортировать (keyset-порядок).
        orders: Порядок сортировки колонок (форма ``SortOrders``); пусто — по возрастанию.
        sort_sources: Источники значений для сортировки (форма ``AttributeSourceTypes``).
        last_key_value: Последнее значение ключевого поля с предыдущей страницы
            (keyset-пагинация; по умолчанию ``0``).
        last_order_value: Последние значения полей сортировки с предыдущей страницы
            (keyset-пагинация; по умолчанию ``null``).
        record_count: Ограничение на число возвращаемых записей (размер страницы).
        conditions: Условия поиска (форма ``SelectConditionDto``).
        local_types_mode: Режим локальных типов объектов (только ``F_GUID`` / ``CAPTION``).
        context_rule: Параметры контекста версий (форма ``ContextRuleDto``).
    """

    relation_type_id: int = Field(description="Идентификатор типа связи (-1 — любой)")
    attribute_ids_to_select: list[int] = Field(
        default_factory=list,
        description="Идентификаторы атрибутов связи для отбора",
    )
    object_type_id: int | None = Field(
        default=None, description="Идентификатор типа объекта (-1 — любой)"
    )
    child_object_types: list[int] | None = Field(
        default=None, description="Идентификаторы типов объектов-потомков"
    )
    attribute_content_overrides: list[Any] | None = Field(
        default=None,
        description="Переопределение содержимого колонок (форма AttributeOverrideContentDto)",
    )
    sort_columns: list[int] | None = Field(
        default=None, description="Идентификаторы атрибутов для сортировки"
    )
    orders: list[Any] | None = Field(
        default=None, description="Порядок сортировки колонок (форма SortOrders)"
    )
    sort_sources: list[Any] | None = Field(
        default=None, description="Источники значений для сортировки (AttributeSourceTypes)"
    )
    last_key_value: int | None = Field(
        default=None, description="Последнее значение ключа (keyset-пагинация)"
    )
    last_order_value: list[Any] | None = Field(
        default=None, description="Последние значения полей сортировки (keyset-пагинация)"
    )
    record_count: int | None = Field(
        default=None, description="Ограничение на число записей (размер страницы)"
    )
    conditions: list[Any] | None = Field(
        default=None, description="Условия поиска (форма SelectConditionDto)"
    )
    local_types_mode: bool | None = Field(
        default=None, description="Режим локальных типов объектов"
    )
    context_rule: dict[str, Any] | None = Field(
        default=None, description="Параметры контекста версий (форма ContextRuleDto)"
    )


class RelationSelectAttributeResult(IPSModel):
    """Значение одного запрошенного атрибута связи (элемент :class:`RelationSelectResult`).

    Возвращается для каждого атрибута из ``attributes_to_select`` / ``attribute_ids_to_select``
    запроса. Форма DTO ``AttributeResultDto``.

    Attributes:
        attribute_id: Идентификатор ТИПА атрибута связи.
        value: Значение атрибута (тип зависит от ``FieldTypes`` атрибута).
    """

    attribute_id: int = Field(description="Идентификатор ТИПА атрибута связи")
    value: Any = Field(default=None, description="Значение атрибута (тип зависит от FieldTypes)")


class RelationSelectResult(IPSModel):
    """Одна найденная связь и значения запрошенных у неё атрибутов.

    Элемент результата расширенного поиска связей (``consist_from`` / ``enters_in`` /
    ``enters_in_version`` / ``relations_select``). Содержит идентификатор связи
    (``relation_id``) и значения запрошенных атрибутов связи.

    Внимание: ``RelationID`` нестабилен — он меняется после ``CheckOut``/``CheckIn``
    родителя, поэтому кэшировать его нельзя (см. граблям); это id-пространство связей,
    отдельное от id объектов и версий.

    Attributes:
        relation_id: Идентификатор найденной связи (JSON-ключ ``relationId``; нестабилен).
        attributes: Значения запрошенных атрибутов связи (``null`` коэрсится в ``[]``).

    Notes:
        Прод-факт: реальный JSON-ключ — ``relationId`` (camelCase), а НЕ ``relationID`` из
        swagger; покрывается генератором ``to_camel`` без явного алиаса.
    """

    relation_id: int = Field(description="Идентификатор связи (нестабилен)")
    attributes: Annotated[list[RelationSelectAttributeResult], EmptyListIfNone] = Field(
        default_factory=list, description="Значения запрошенных атрибутов связи"
    )

    @property
    def values(self) -> dict[int, Any]:
        """Возвращает значения атрибутов связи как словарь ``{attribute_id: value}``.

        Удобный доступ к значениям по id типа атрибута вместо обхода ``attributes``.
        При повторе одного ``attribute_id`` останется последнее значение.

        Returns:
            Словарь ``{attribute_id: value}`` по всем элементам ``attributes`` (пустой,
            если атрибуты не запрашивались).
        """
        return {a.attribute_id: a.value for a in self.attributes}
