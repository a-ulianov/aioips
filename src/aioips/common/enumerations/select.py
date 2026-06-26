"""Перечисления для поиска объектов (``objects/select``).

Значения соответствуют enum'ам ``RelationalOperators``, ``LogicalOperators`` и
``ColumnContents`` из IPS Web API.
"""

from enum import StrEnum


class RelationalOperator(StrEnum):
    """Оператор сравнения в условии поиска ``objects/select`` (``RelationalOperators``).

    Задаёт, как сравнивать значение атрибута (``Attribute``) с эталоном
    (``Value``/``Value2``) в одном условии. Применяй при сборке
    ``ConditionStructure`` для поиска объектов. Для ссылки на объект сравнивай
    по id (``ColumnContent.ID``) с оператором ``EQUAL``.

    Ключевые члены:
        EQUAL / NOT_EQUAL: ``equal`` / ``notEqual`` — точное (не)совпадение.
        GREATER / GREATER_OR_EQUAL / LESS / LESS_OR_EQUAL: числовые/датовые сравнения.
        SUBSTRING: ``substring`` — атрибут содержит подстроку.
        START_STRING / END_STRING: ``startString`` / ``endString`` — начинается/кончается.
        BETWEEN: ``between`` — значение в диапазоне ``Value``..``Value2``.
        STRING_TEMPLATE: ``stringTemplate`` — шаблон с ``?``/``*``.
        IN / NOT_IN: ``in`` / ``notIn`` — (не)вхождение в перечень значений.
        IN_SELECTION: ``inSelection`` — объект состоит в именованной выборке.
        ENTERS_IN: ``entersIn`` — объект входит в состав указанного объекта.
        CONSIST_FROM: ``consistFrom`` — объект состоит из указанного объекта.
        EMPTY / NOT_EMPTY: ``empty`` / ``notEmpty`` — значение (не) пустое.
        ATTRIBUTE_EXISTS: ``attributeExists`` — атрибут присутствует у объекта.
        LAST_N_DAYS / NEXT_N_DAYS: ``lastNDays`` / ``nextNDays`` — окно по дате.
        MAX_VERSION / MIN_VERSION: ``maxVersion`` / ``minVersion`` — крайняя версия.

    Notes:
        Перечислены не все значения; остальные члены — узкоспециальные фильтры
        (типы, версии, история ЖЦ, индексы). Полный набор — в членах класса.

    References:
        Операторы поиска — [[ips-object-model]] (раздел «Поиск»).
    """

    EMPTY = "empty"
    NOT_EMPTY = "notEmpty"
    EQUAL = "equal"
    NOT_EQUAL = "notEqual"
    GREATER = "greater"
    GREATER_OR_EQUAL = "greaterOrEqual"
    LESS = "less"
    LESS_OR_EQUAL = "lessOrEqual"
    SUBSTRING = "substring"
    START_STRING = "startString"
    END_STRING = "endString"
    BETWEEN = "between"
    NOT_SUBSTRING = "notSubstring"
    NOT_START_STRING = "notStartString"
    NOT_END_STRING = "notEndString"
    NOT_BETWEEN = "notBetween"
    ENTERS_IN = "entersIn"
    CONSIST_FROM = "consistFrom"
    NOT_ENTERS_IN_TYPE = "notEntersInType"
    ENTERS_IN_TYPE = "entersInType"
    IN = "in"
    IN_SELECTION = "inSelection"
    NOP = "nop"
    CONSIST_FROM_TYPE = "consistFromType"
    NOT_CONSIST_FROM_TYPE = "notConsistFromType"
    PARENT_VERSION_ID = "parentVersionID"
    OBJECT_TYPE_FILTER = "objectTypeFilter"
    ATTRIBUTE_EXISTS = "attributeExists"
    LAST_N_DAYS = "lastNDays"
    NOT_IN = "notIn"
    NOT_EXISTS_OR_EMPTY = "notExistsOrEmpty"
    EXISTS_IN_VERSION_CONTEXT = "existsInVersionContext"
    STRING_TEMPLATE = "stringTemplate"
    IN_GLOBAL_INDEX = "inGlobalIndex"
    IN_FILTRATION_TABLE = "inFiltrationTable"
    NEXT_N_DAYS = "nextNDays"
    IN_LC_HISTORY = "inLCHistory"
    LINKED = "linked"
    NOT_LINKED = "notLinked"
    LOCAL_OBJECT_TYPES = "localObjectTypes"
    MAX_VERSION = "maxVersion"
    MIN_VERSION = "minVersion"
    NONE = "none"


class LogicalOperator(StrEnum):
    """Логическая связь условия с предыдущим в наборе (``LogicalOperators``).

    Задаётся в каждом условии ``ConditionStructure`` и определяет, как оно
    соединяется с накопленным результатом; скобки группировки — через ``GroupID``.

    Семантика членов:
        NONE: ``none`` — связь не задана (первое условие).
        OR: ``or`` — логическое ИЛИ с предыдущим.
        AND: ``and`` — логическое И с предыдущим.
        NOT: ``not`` — логическое отрицание условия.
    """

    NONE = "none"
    OR = "or"
    AND = "and"
    NOT = "not"


class ColumnContent(StrEnum):
    """Как интерпретировать значение условия/колонки поиска (``ColumnContents``).

    Указывает, в каком представлении сравнивать атрибут: текст, id, дата и т.п.
    Для условий по ссылочным атрибутам (``ftObjectLink``) используй ``ID`` —
    сравнение идёт по id связанного объекта (например, поиск документов архива).

    Семантика членов:
        TEXT: ``text`` — текстовое (отображаемое) представление.
        ID: ``id`` — сравнение по идентификатору (в т.ч. id связанного объекта).
        DATE: ``date`` — значение как дата.
        VALUE: ``value`` — «сырое» типизированное значение атрибута.
        STRING: ``string`` — строковое представление значения.
    """

    TEXT = "text"
    ID = "id"
    DATE = "date"
    VALUE = "value"
    STRING = "string"
