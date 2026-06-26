"""Схемы информации об индексах справочной системы IMBASE.

References:
    ``GET /core/api/imbase/indexes`` — ``ImBaseIndexesInfoDto`` (с вложенными
    ``ImBaseCatalogInfoDto`` и ``ImBaseIndexInfoDto``).
"""

from typing import Annotated

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class ImBaseCatalogInfo(IPSModel):
    """Сведения о каталоге IMBASE, содержащем индекс.

    Каталог IMBASE — узел справочной системы (тип отражён в ``type``: каталог,
    классификатор и т.п.), для которого определены индексы атрибутов. Используется
    как элемент списка ``catalogs`` в :class:`ImBaseIndexesInfo`.

    Attributes:
        id: Идентификатор каталога.
        name: Наименование каталога.
        type: Тип каталога (системное строковое значение: каталог, классификатор и т.п.).
    """

    id: int = Field(description="Идентификатор каталога")
    name: str = Field(description="Наименование каталога")
    type: str = Field(description="Тип каталога (каталог, классификатор и т.п.)")


class ImBaseIndexInfo(IPSModel):
    """Сведения об одном индексе IMBASE: каталог и индексируемый атрибут.

    Описывает связку «каталог → проиндексированный атрибут». Используется как элемент
    списка ``indexes`` в :class:`ImBaseIndexesInfo`. ``catalog_id`` ссылается на
    каталог из ``catalogs`` (см. :class:`ImBaseCatalogInfo`).

    Attributes:
        catalog_id: Идентификатор каталога, к которому относится индекс.
        attribute_id: Идентификатор проиндексированного атрибута.
    """

    catalog_id: int = Field(description="Идентификатор каталога, содержащего индекс")
    attribute_id: int = Field(description="Идентификатор проиндексированного атрибута")


class ImBaseIndexesInfo(IPSModel):
    """Информация об индексах справочной системы IMBASE: каталоги и их индексы.

    Объединяет перечень каталогов, для которых заданы индексы, и список самих индексов
    (каждый — пара «каталог + атрибут»). Применяется для понимания, по каким атрибутам
    каких каталогов возможен индексный поиск IMBASE.

    Когда применять: чтобы определить доступность индексного поиска перед его вызовом,
    либо для построения карты «каталог → индексируемые атрибуты». Отдаётся методом
    :meth:`imbase_indexes`; те же данные входят в :class:`ImBaseClientCacheState`
    (поле ``indexes_info``).

    Attributes:
        catalogs: Список каталогов IMBASE, содержащих индексы.
        indexes: Список индексов (пары «каталог + атрибут»).
    """

    catalogs: Annotated[list[ImBaseCatalogInfo], EmptyListIfNone] = Field(
        default_factory=list, description="Каталоги IMBASE, содержащие индексы"
    )
    indexes: Annotated[list[ImBaseIndexInfo], EmptyListIfNone] = Field(
        default_factory=list, description="Индексы IMBASE (пары «каталог + атрибут»)"
    )
