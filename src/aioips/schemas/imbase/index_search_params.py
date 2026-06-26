"""Схема параметров индексного (полнотекстового) поиска по атрибуту IMBASE.

References:
    ``POST /core/api/imbase/find/byIndex`` — тело запроса
    ``ImBaseIndexSearchParamsDto``; точность поиска — enum ``SearchesAccuracy``.
"""

from typing import Annotated

from pydantic import Field

from ...common.enumerations import SearchesAccuracy
from ..base import EmptyListIfNone, IPSModel


class ImBaseIndexSearchParams(IPSModel):
    """Параметры индексного поиска по атрибуту IMBASE (``ImBaseIndexSearchParamsDto``).

    Тело запроса для метода :meth:`imbase_find_by_index`. Задаёт индексируемый атрибут,
    поисковую строку, точность совпадения и область поиска (каталоги/папка). Несмотря на
    HTTP-метод POST, метод-получатель выполняет ЧТЕНИЕ — тело несёт параметры поиска,
    сервер ничего не изменяет.

    Точность ``search_accuracy`` — строковый enum ``SearchesAccuracy`` со значениями
    ``"start"`` (с начала), ``"contain"`` (вхождение), ``"end"`` (с конца),
    ``"exact"`` (точное), ``"template"`` (по шаблону); тип оставлен ``str | None``,
    чтобы не требовать импорта enum. ``catalog_ids`` и ``start_folder_id`` —
    взаимоисключающая область: если задан список каталогов, ``start_folder_id`` не
    используется (значение ``0`` — поиск по всей базе IMBASE).

    Все поля имеют дефолты. Сериализуйте тело как
    ``model_dump(mode="json", by_alias=True, exclude_none=True)``.

    Attributes:
        attribute_id: Идентификатор индексируемого атрибута (``attributeId``, int),
            по которому ведётся поиск. По умолчанию ``0``.
        search_query: Поисковая строка (``searchQuery``); для пустого поиска можно
            передать пустую строку. По умолчанию ``None``.
        search_accuracy: Точность совпадения (``searchAccuracy``, enum
            ``SearchesAccuracy``: ``start``/``contain``/``end``/``exact``/``template``)
            как ``str``. По умолчанию ``None``.
        catalog_ids: Идентификаторы каталогов IMBASE области поиска (``catalogIds``,
            list[int]); ``null`` нормализуется в пустой список. Если задан — поиск по
            этим каталогам и их подкаталогам, ``start_folder_id`` игнорируется.
            По умолчанию пустой список.
        start_folder_id: Идентификатор папки IMBASE — корня поиска (``startFolderId``,
            int|None); ``0`` или ``None`` — без ограничения папкой. По умолчанию ``None``.
        result_count_limit: Ограничение на число результатов (``resultCountLimit``,
            int|None); ``None`` — без ограничения. По умолчанию ``None``.
    """

    attribute_id: int = Field(
        default=0,
        alias="attributeId",
        description="Идентификатор индексируемого атрибута",
    )
    search_query: str | None = Field(
        default=None,
        alias="searchQuery",
        description="Поисковая строка",
    )
    search_accuracy: SearchesAccuracy | str | None = Field(
        default=None,
        alias="searchAccuracy",
        description="Точность совпадения (enum SearchesAccuracy)",
    )
    catalog_ids: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list,
        alias="catalogIds",
        description="Идентификаторы каталогов IMBASE области поиска",
    )
    start_folder_id: int | None = Field(
        default=None,
        alias="startFolderId",
        description="Идентификатор папки IMBASE — корня поиска",
    )
    result_count_limit: int | None = Field(
        default=None,
        alias="resultCountLimit",
        description="Ограничение на число результатов",
    )
