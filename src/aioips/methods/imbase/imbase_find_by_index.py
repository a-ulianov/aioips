"""Метод индексного (полнотекстового) поиска по атрибуту IMBASE (чтение через POST)."""

from typing import Any

from ...core import APIManager
from ...schemas.imbase.index_search_params import ImBaseIndexSearchParams


class ImBaseFindByIndexMixin(APIManager):
    """Реализует ``POST /core/api/imbase/find/byIndex``.

    operationId ``ImBase_FindByIndex``.
    """

    async def imbase_find_by_index(
        self: "ImBaseFindByIndexMixin",
        params: ImBaseIndexSearchParams,
    ) -> list[dict[str, Any]]:
        """Выполняет индексный (полнотекстовый) поиск по атрибуту IMBASE (чтение).

        Ищет объекты/записи IMBASE по индексированному атрибуту: поисковую строку, точность
        совпадения и область поиска (каталоги или папка) задаёт тело
        :class:`ImBaseIndexSearchParams`. Несмотря на HTTP-метод POST, это операция ЧТЕНИЯ —
        сервер ничего не изменяет, тело служит контейнером параметров.

        Когда применять: для быстрого полнотекстового/префиксного поиска по одному
        индексируемому атрибуту (например, найти материалы по фрагменту обозначения).
        Родственный метод :meth:`imbase_find_in_tables` ищет записи таблиц по набору
        условий. Предусловий нет (операция чтения).

        Args:
            params: Параметры поиска (:class:`ImBaseIndexSearchParams`): ``attribute_id``,
                ``search_query``, ``search_accuracy`` (enum ``SearchesAccuracy``),
                область поиска ``catalog_ids`` / ``start_folder_id`` и ограничение
                ``result_count_limit``.

        Returns:
            Список найденных элементов как ``list[dict[str, Any]]`` по DTO
            ``ImBaseIndexSearchResultEntryDto``. Ответ обёрнут в
            ``...IEnumerableNullableResultDto`` (``{entity, isEntityPresent}``); обёртка
            разворачивается здесь. Пустой список — ничего не найдено либо ``entity``
            отсутствует/``None``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                params = ImBaseIndexSearchParams(
                    attribute_id=1029,
                    search_query="550.07",
                    search_accuracy="start",
                    catalog_ids=[12, 34],
                    result_count_limit=50,
                )
                hits = await ips.imbase_find_by_index(params)
                print(len(hits))

        Notes:
            operationId ``ImBase_FindByIndex``; путь ``POST /core/api/imbase/find/byIndex``;
            тело — ``ImBaseIndexSearchParamsDto``; ответ —
            ``ImBaseIndexSearchResultEntryDtoIEnumerableNullableResultDto`` (entity-массив).
            См. [[ips-object-model]].
        """
        payload = params.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/imbase/find/byIndex", json=payload)
        entity = data.get("entity") if isinstance(data, dict) else None
        if not isinstance(entity, list):
            return []
        return [item for item in entity if isinstance(item, dict)]
