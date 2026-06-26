"""Схемы истории значений атрибутов IPS.

История значений атрибута — это журнал того, как менялось значение конкретного
атрибута: какое значение установлено, когда и каким пользователем. Запрос истории
и её удаление используют одно и то же тело :class:`AttributeHistoryRequest`,
а чтение возвращает список элементов :class:`AttributeHistoryValue`.

References:
    ``POST /core/api/attributeHistory/getHistory`` — ``AtributeHistory_GetAttributeHistory``;
    ``POST /core/api/attributeHistory/deleteHistory`` — ``AtributeHistory_DeleteHistory``.
"""

from datetime import datetime
from enum import StrEnum

from pydantic import Field

from ..base import IPSModel


class HistoryType(StrEnum):
    """Область действия запроса/удаления истории атрибута (``HistoryType``).

    Определяет, к какому множеству носителей применяется операция: к одному
    объекту/связи, ко всем объектам того же типа или ко всем объектам вообще.
    Используется в поле ``history_type`` запроса :class:`AttributeHistoryRequest`;
    особенно важна для удаления, так как расширяет область необратимого действия.

    Семантика членов:
        FOR_OBJECT: ``forObject`` — история для конкретного объекта/связи (по ``id``).
        FOR_SAME_TYPE: ``forSameType`` — история по всем объектам того же типа (``type_id``).
        FOR_ALL_TYPE: ``forAllType`` — история по всем объектам (без ограничения типом).
    """

    FOR_OBJECT = "forObject"
    FOR_SAME_TYPE = "forSameType"
    FOR_ALL_TYPE = "forAllType"


class AttributeHistoryRequest(IPSModel):
    """Запрос истории значений атрибута (тело ``getHistory``/``deleteHistory``).

    Однозначно адресует историю изменений: какой атрибут (``attribute_id``), у
    какого носителя (объект или связь — ``is_relation``, идентификатор ``id``,
    тип ``type_id``) и какую область охватить (``history_type``). Одно и то же
    тело применяется и для чтения истории (:meth:`attribute_history`), и для её
    удаления (:meth:`delete_attribute_history`).

    Предусловия и грабли по id-пространству: ``id`` — это идентификатор носителя
    значения (для объекта — версия, F_ID; для связи — id связи), а не id типа.
    Поле ``type_id`` задаёт тип объекта/связи и определяет область для
    ``history_type=FOR_SAME_TYPE``. ``is_relation`` различает, относится ли атрибут
    к объекту или к связи.

    Attributes:
        attribute_id: Идентификатор ТИПА атрибута, историю которого читать/удалять.
        is_relation: ``True`` — атрибут связи, ``False`` — атрибут объекта.
        id: Идентификатор носителя значения (объект/версия или связь). Для
            ``history_type=FOR_OBJECT`` адресует конкретный носитель.
        type_id: Идентификатор типа объекта/связи. Задаёт область для
            ``history_type=FOR_SAME_TYPE``.
        only_personal: Ограничить операцию персональной историей текущего
            пользователя (а не общей).
        history_type: Область действия (см. :class:`HistoryType`): один носитель,
            все носители типа или все носители.
    """

    attribute_id: int = Field(description="Идентификатор ТИПА атрибута")
    is_relation: bool = Field(default=False, description="Атрибут связи (True) или объекта (False)")
    id: int = Field(default=0, description="Идентификатор носителя значения (объект/версия/связь)")
    type_id: int = Field(default=0, description="Идентификатор типа объекта/связи")
    only_personal: bool = Field(
        default=False, description="Только персональная история текущего пользователя"
    )
    history_type: HistoryType = Field(
        default=HistoryType.FOR_OBJECT, description="Область действия (HistoryType)"
    )


class AttributeHistoryValue(IPSModel):
    """Один элемент истории значений атрибута (кто/когда/какое значение).

    Возвращается списком из :meth:`attribute_history`. Каждый элемент фиксирует
    одно состояние атрибута во времени: установленное значение (``value`` —
    текстовое представление), момент изменения (``date``) и пользователя,
    выполнившего изменение (``user``).

    Все поля необязательны и могут отсутствовать (``None``): IPS может не знать
    автора или не хранить точную дату для отдельных записей.

    Attributes:
        date: Дата/время изменения значения (UTC). ``None`` — момент неизвестен.
        value: Текстовое представление значения атрибута на этот момент.
            ``None`` — значение было очищено/пустое.
        user: Имя пользователя, изменившего значение. ``None`` — автор неизвестен.
    """

    date: datetime | None = Field(default=None, description="Дата/время изменения значения (UTC)")
    value: str | None = Field(default=None, description="Текстовое представление значения")
    user: str | None = Field(default=None, description="Пользователь, изменивший значение")
