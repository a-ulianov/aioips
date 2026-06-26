"""Схемы поиска объектов (``objects/select``).

Поиск задаётся типом объекта и набором условий по атрибутам (:class:`SelectCondition`).
Возвращается список найденных объектов (:class:`ObjectSelectResult`) с идентификаторами
и значениями запрошенных атрибутов (:class:`AttributeResult`). Поиск по атрибуту-ссылке
ведётся через ``content=ID`` по id связанного объекта — так находят, например, документы
конкретного архива. См. [[ips-object-model]] (раздел «Поиск») и [[gotchas]].

References:
    ``POST /core/api/objects/select`` — ``Objects_GetSelectsObjects``.
"""

from typing import Annotated, Any

from pydantic import Field

from ...common.enumerations.select import (
    ColumnContent,
    LogicalOperator,
    RelationalOperator,
)
from ..base import EmptyListIfNone, IPSModel


class SelectCondition(IPSModel):
    """Условие поиска по значению атрибута (элемент запроса ``objects_select``).

    Одно условие = сравнение значения атрибута (``attribute_id``) с эталоном (``value``)
    через оператор (``relational_operator``). Несколько условий объединяются логическими
    операторами (``logical_operator``) и группируются скобками (``group_id``).

    Важно для атрибутов-ссылок (``ftObjectLink``): чтобы найти объекты по ссылке (напр.
    документы конкретного архива), задайте ``content=ColumnContent.ID`` и в ``value``
    передайте id связанного объекта (id архива) — сравнение пойдёт по id, не по тексту.

    Attributes:
        attribute_id: Идентификатор ТИПА атрибута, по которому строится условие.
        relational_operator: Оператор сравнения (напр. ``EQUAL``, ``SUBSTRING``, ``BETWEEN``).
        value: Сравниваемое значение (тип зависит от атрибута и оператора).
        value2: Второе значение для диапазонных операторов (``BETWEEN``).
        content: Как интерпретировать значение (``ID`` для ссылок, ``TEXT``/``STRING`` и т.п.).
        logical_operator: Логическая связь со следующим условием (по умолчанию ``AND``).
        group_id: Идентификатор группы условий (для скобочной логики; по умолчанию 0).
        case_sensitive: Учитывать регистр при строковом сравнении (по умолчанию ``False``).
    """

    attribute_id: int = Field(description="Идентификатор ТИПА атрибута")
    relational_operator: RelationalOperator = Field(
        description="Оператор сравнения (RelationalOperator)"
    )
    value: Any = Field(
        default=None, description="Сравниваемое значение (для content=ID — id связанного объекта)"
    )
    value2: Any = Field(default=None, description="Второе значение (для BETWEEN)")
    content: ColumnContent | None = Field(
        default=None, description="Как интерпретировать значение (ColumnContent; ID для ссылок)"
    )
    logical_operator: LogicalOperator = Field(
        default=LogicalOperator.AND, description="Логическая связь со следующим условием"
    )
    group_id: int = Field(
        default=0, alias="groupID", description="Группа условий (скобочная логика)"
    )
    case_sensitive: bool = Field(
        default=False, description="Учитывать регистр при строковом сравнении"
    )


class AttributeResult(IPSModel):
    """Значение одного запрошенного атрибута у найденного объекта.

    Возвращается в составе :class:`ObjectSelectResult` для каждого атрибута из
    ``attribute_ids`` запроса ``objects_select``.

    Attributes:
        attribute_id: Идентификатор ТИПА атрибута.
        value: Значение атрибута (тип зависит от ``FieldTypes`` атрибута).
    """

    attribute_id: int = Field(description="Идентификатор ТИПА атрибута")
    value: Any = Field(default=None, description="Значение атрибута (тип зависит от FieldTypes)")


class ObjectSelectResult(IPSModel):
    """Один найденный объект и значения запрошенных у него атрибутов.

    Элемент результата ``objects_select``. Идентификатор возвращается в поле
    ``object_id`` (как его сериализует сервер поиска); чтобы затем загрузить объект
    целиком, используйте :class:`ObjectDto`-методы (например ``object_get``), сверяя
    id-пространство по [[ips-object-model]].

    Attributes:
        object_id: Идентификатор найденного объекта (как его отдаёт ``objects/select``).
        attributes: Значения запрошенных атрибутов (по списку ``attribute_ids``).
    """

    object_id: int = Field(
        description="Идентификатор найденного объекта (как его отдаёт objects/select)"
    )
    attributes: Annotated[list[AttributeResult], EmptyListIfNone] = Field(
        default_factory=list, description="Значения запрошенных атрибутов (по attribute_ids)"
    )

    @property
    def values(self) -> dict[int, Any]:
        """Возвращает значения атрибутов в виде словаря ``{attribute_id: value}``.

        Удобный доступ к значениям по id типа атрибута вместо обхода ``attributes``.
        При повторе одного ``attribute_id`` останется последнее значение.

        Returns:
            Словарь ``{attribute_id: value}`` по всем элементам ``attributes`` (пустой,
            если атрибуты не запрашивались).
        """
        return {a.attribute_id: a.value for a in self.attributes}
