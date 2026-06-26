"""Схема параметров поиска записей в таблицах справочника IMBASE.

References:
    ``POST /core/api/imbase/find/inTables`` ·
    ``POST /core/api/imbase/attribute/byGuid/{attributeGuid}/existingValues`` —
    тело запроса ``ImBaseTableSearchParamsDto``; условия — ``TableFilterConditionItemDto``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class ImBaseTableSearchParams(IPSModel):
    """Параметры поиска записей в таблицах справочника IMBASE (``ImBaseTableSearchParamsDto``).

    Тело запроса для методов :meth:`imbase_find_in_tables` и
    :meth:`imbase_attribute_existing_values`. Описывает, в каких таблицах IMBASE
    искать (``table_links_lookup``) и по каким условиям (``conditions``). Несмотря
    на HTTP-метод POST, методы-получатели выполняют ЧТЕНИЕ — тело служит контейнером
    параметров поиска, сервер ничего не изменяет.

    Структура ``conditions`` (``TableFilterConditionItemDto``) вложенная и зависит от
    типа атрибута и оператора сравнения (поля ``attributeId``, ``condition``, ``data``,
    ``data2``), поэтому типизируется как ``list[dict[str, Any]]`` — передавайте
    сырые словари условий. ``table_links_lookup`` — словарь «id таблицы IMBASE → список
    id записей таблицы IMBASE», задающий область поиска.

    Все поля имеют дефолты (пустая коллекция): пустой поиск вернёт результат по всем
    доступным записям без дополнительных ограничений. Сериализуйте тело как
    ``model_dump(mode="json", by_alias=True, exclude_none=True)``.

    Attributes:
        table_links_lookup: Словарь ``tableLinksLookup`` вида «id таблицы IMBASE
            (строка) → список id записей таблицы IMBASE (int)», задающий область поиска;
            ``null`` нормализуется в пустой словарь. По умолчанию пустой словарь.
        conditions: Список условий фильтрации (``conditions``,
            ``TableFilterConditionItemDto``: ``attributeId``/``condition``/``data``/
            ``data2``) как ``list[dict[str, Any]]``; ``null`` нормализуется в пустой
            список. По умолчанию пустой список.
    """

    table_links_lookup: dict[str, list[int]] = Field(
        default_factory=dict,
        alias="tableLinksLookup",
        description="id таблицы IMBASE → список id записей таблицы IMBASE",
    )
    conditions: Annotated[list[dict[str, Any]], EmptyListIfNone] = Field(
        default_factory=list,
        description="Условия фильтрации записей таблиц IMBASE",
    )
