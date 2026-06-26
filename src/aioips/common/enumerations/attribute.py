"""Перечисления, относящиеся к типам и значениям атрибутов IPS.

Значения сверены с enum'ами ``FieldTypes``, ``MultiValueModes`` и ``ComputeValueModes``
из IPS Web API. Семантику типов см. в объектной модели IPS.
"""

from enum import StrEnum


class FieldType(StrEnum):
    """Тип данных атрибута IPS (``FieldTypes``, 18 значений).

    Определяет, как хранится и интерпретируется значение атрибута объекта или
    связи. Приходит в метаданных атрибута (``object_attributes``) и определяет,
    как читать значение: для ссылочных типов читают id/GUID, а не сам объект.
    Применяй при разборе схемы атрибутов и при формировании условий поиска.

    Семантика членов:
        UNKNOWN: ``ftUnknown`` — тип не определён.
        STRING: ``ftString`` — строка до 450 символов.
        INTEGER: ``ftInteger`` — целое (Int64).
        DOUBLE: ``ftDouble`` — число с плавающей точкой.
        DATE_TIME: ``ftDateTime`` — дата/время (хранится в UTC).
        SHORT_BLOB: ``ftShortBlob`` — небольшой двоичный блок (≤~128 КБ в БД).
        FILE: ``ftFile`` — файл во внешнем хранилище/vault (диск X:).
        EXTERNAL_LINK: ``ftExternalLink`` — внешняя ссылка (URL/путь).
        OBJECT_LINK: ``ftObjectLink`` — ссылка на объект; значение = id
            объекта-цели (так задаётся, например, «документ → Архив»).
        PASSWORD: ``ftPassword`` — хэш пароля.
        MEMO: ``ftMemo`` — длинный текст.
        BLOB: ``ftBlob`` — двоичные данные в БД.
        BOOLEAN: ``ftBoolean`` — логическое значение.
        MEASURED: ``ftMeasured`` — измеряемая величина (число + единица измерения).
        AUTO_INC: ``ftAutoInc`` — автоинкрементное значение.
        SYSTEM: ``ftSystem`` — системный обязательный атрибут.
        GUID: ``ftGuid`` — глобальный идентификатор.
        OBJECT_LINK_BY_ID: ``ftObjectLinkByID`` — ссылка на объект по id версии.

    References:
        Типы данных и хранение — объектной модели IPS (раздел «Атрибуты»).
    """

    UNKNOWN = "ftUnknown"
    STRING = "ftString"
    INTEGER = "ftInteger"
    DOUBLE = "ftDouble"
    DATE_TIME = "ftDateTime"
    SHORT_BLOB = "ftShortBlob"
    FILE = "ftFile"
    EXTERNAL_LINK = "ftExternalLink"
    OBJECT_LINK = "ftObjectLink"
    PASSWORD = "ftPassword"  # noqa: S105 — имя типа атрибута, не секрет
    MEMO = "ftMemo"
    BLOB = "ftBlob"
    BOOLEAN = "ftBoolean"
    MEASURED = "ftMeasured"
    AUTO_INC = "ftAutoInc"
    SYSTEM = "ftSystem"
    GUID = "ftGuid"
    OBJECT_LINK_BY_ID = "ftObjectLinkByID"


class MultiValueMode(StrEnum):
    """Режим множественности значений атрибута (``MultiValueModes``).

    Определяет, сколько значений может иметь атрибут и ограничен ли набор
    значений списком допустимых. У режимов ``…FromList`` значения берутся из
    набора, возвращаемого ``GetPossibleValues()`` в ядре IPS.

    Семантика членов:
        SINGLE_VALUE: ``singleValue`` — ровно одно значение.
        MULTI_VALUES: ``multiValues`` — несколько произвольных значений.
        SINGLE_VALUE_FROM_LIST: ``singleValueFromList`` — одно значение из списка.
        MULTI_VALUES_FROM_LIST: ``multiValuesFromList`` — несколько значений из списка.
    """

    SINGLE_VALUE = "singleValue"
    MULTI_VALUES = "multiValues"
    SINGLE_VALUE_FROM_LIST = "singleValueFromList"
    MULTI_VALUES_FROM_LIST = "multiValuesFromList"


class ComputeValueMode(StrEnum):
    """Режим вычисления значения атрибута (``ComputeValueModes``).

    Указывает, как формируется значение атрибута: хранится явно, вычисляется
    на лету или служит индексом. Влияет на возможность записи значения.

    Семантика членов:
        NOT_COMPUTABLE: ``notComputableValue`` — значение не вычисляется.
        STORED: ``storedValue`` — вычисляемое, но сохранённое значение.
        JIT: ``jitValue`` — вычисляется по запросу (just-in-time).
        INDEX: ``indexValue`` — индексное (вычисляемое) значение.
    """

    NOT_COMPUTABLE = "notComputableValue"
    STORED = "storedValue"
    JIT = "jitValue"
    INDEX = "indexValue"
