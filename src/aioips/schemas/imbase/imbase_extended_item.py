"""Схема расширенных настроек типа атрибута, связанного с IMBASE.

References:
    ``GET /core/api/imbase/extendedItem/{attributeTypeId}`` — ``ImBaseExtendedItemDto``
    (внутри обёртки ``...NullableResultDto``).
"""

from typing import Annotated

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class ImBaseExtendedItem(IPSModel):
    """Расширенные настройки типа атрибута, связанного со справочником IMBASE.

    Описывает, из каких каталогов IMBASE можно выбирать значения для данного типа
    атрибута и в каком режиме выбора. Применяется при построении выпадающих
    списков/диалогов выбора значения атрибута, ссылающегося на IMBASE.

    Когда применять: при подготовке UI выбора значения атрибута-ссылки на IMBASE —
    чтобы знать допустимые каталоги и режим выбора. Отдаётся методом
    :meth:`imbase_extended_item` (принимает id ТИПА атрибута).

    ``catalog_ids`` — идентификаторы ВЕРСИЙ каталогов IMBASE. Значения
    ``select_mode`` (enum ``ImbaseCatalogSelectMode`` из swagger):
    ``imcmSelectFolder`` (выбор папки справочника), ``imcmCreateObject`` (создание
    объекта по справочнику), ``imcmNone`` (нет), ``imcmAllowSelectRow`` (выбор записи
    в таблице IMBASE). Поле типизировано как ``str`` для совместимости.

    Attributes:
        catalog_ids: Идентификаторы версий каталогов IMBASE, из которых возможен
            выбор значений атрибута.
        select_mode: Режим выбора объектов из каталогов IMBASE (см. значения выше).
    """

    catalog_ids: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list,
        description="Id версий каталогов IMBASE для выбора значений атрибута",
    )
    select_mode: str = Field(description="Режим выбора объектов из каталогов IMBASE")
