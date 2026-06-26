"""Метод поиска записей в таблицах справочника IMBASE по условиям (чтение через POST)."""

from typing import Any

from ...core import APIManager
from ...schemas.imbase.table_search_params import ImBaseTableSearchParams


class ImBaseFindInTablesMixin(APIManager):
    """Реализует ``POST /core/api/imbase/find/inTables``.

    operationId ``ImBase_FindInTables``.
    """

    async def imbase_find_in_tables(
        self: "ImBaseFindInTablesMixin",
        params: ImBaseTableSearchParams,
    ) -> list[dict[str, Any]]:
        """Ищет записи в таблицах справочника IMBASE по заданным условиям (чтение).

        Выполняет поиск по табличным частям справочника IMBASE: область поиска и условия
        фильтрации задаёт тело :class:`ImBaseTableSearchParams` (словарь «таблица → записи»
        и список условий по атрибутам). Несмотря на HTTP-метод POST, это операция ЧТЕНИЯ —
        сервер ничего не изменяет, тело служит контейнером параметров.

        Когда применять: чтобы найти конкретные записи таблиц IMBASE, удовлетворяющие
        набору условий (например, выбрать строки рецептуры по марке материала). Родственный
        метод :meth:`imbase_find_by_index` выполняет полнотекстовый/индексный поиск по
        одному атрибуту. Предусловий нет (операция чтения).

        Args:
            params: Параметры поиска (:class:`ImBaseTableSearchParams`): область поиска
                ``table_links_lookup`` (id таблицы → id записей) и условия фильтрации
                ``conditions``.

        Returns:
            Список найденных записей как ``list[dict[str, Any]]`` по DTO
            ``ImBaseTableSearchResultEntryDto`` (каждый элемент содержит ``linkId`` —
            id связи/таблицы IMBASE и ``recordIds`` — id записей). Ответ — голый массив;
            пустой список — ничего не найдено.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                params = ImBaseTableSearchParams(
                    table_links_lookup={"204": [1, 2, 3]},
                    conditions=[{"attributeId": 1029, "condition": "eq", "data": "Сталь"}],
                )
                entries = await ips.imbase_find_in_tables(params)
                for entry in entries:
                    print(entry["linkId"], entry["recordIds"])

        Notes:
            operationId ``ImBase_FindInTables``; путь ``POST /core/api/imbase/find/inTables``;
            тело — ``ImBaseTableSearchParamsDto``; ответ — массив
            ``ImBaseTableSearchResultEntryDto`` (без result-обёртки). См. объектной модели IPS.
        """
        payload = params.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/imbase/find/inTables", json=payload)
        items = data if isinstance(data, list) else []
        return [item for item in items if isinstance(item, dict)]
