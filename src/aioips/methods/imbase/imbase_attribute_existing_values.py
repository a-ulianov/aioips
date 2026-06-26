"""Метод получения существующих значений атрибута в таблицах IMBASE (чтение через POST)."""

from typing import Any

from ...core import APIManager
from ...schemas.imbase.table_search_params import ImBaseTableSearchParams


class ImBaseAttributeExistingValuesMixin(APIManager):
    """Реализует ``POST .../imbase/attribute/byGuid/{attributeGuid}/existingValues``.

    operationId ``ImBase_GetTableSearchExistingAttributeValues``.
    """

    async def imbase_attribute_existing_values(
        self: "ImBaseAttributeExistingValuesMixin",
        attribute_guid: str,
        params: ImBaseTableSearchParams,
    ) -> dict[str, Any]:
        """Возвращает существующие значения атрибута в таблицах IMBASE (чтение).

        Для заданного атрибута собирает множество уже встречающихся в таблицах справочника
        IMBASE значений — основу для подсказок/выпадающих списков при фильтрации. Область
        поиска и условия задаёт тело :class:`ImBaseTableSearchParams`. Несмотря на
        HTTP-метод POST, это операция ЧТЕНИЯ — сервер ничего не изменяет.

        Когда применять: при построении интерфейса фильтра по таблице справочника — чтобы
        показать только реально существующие значения атрибута. Родственный метод
        :meth:`imbase_find_in_tables` ищет сами записи по условиям. Предусловий нет
        (операция чтения).

        Args:
            attribute_guid: GUID ТИПА атрибута (``attributeGuid``, id-пространство типов
                атрибутов — GUID, не числовой id и не id записи), для которого собираются
                значения.
            params: Параметры области поиска (:class:`ImBaseTableSearchParams`): таблицы
                ``table_links_lookup`` и условия ``conditions``.

        Returns:
            Опаковая структура существующих значений как ``dict[str, Any]`` по DTO
            ``ImBaseTableSearchExistingAttributeValuesDto`` (поле ``values`` — массив
            значений; ``linkValuesNames`` — словарь «id/guid значения-ссылки → подпись»
            для атрибутов-ссылок ``ftObjectLink``/``ftObjectLinkByID``). Структура
            неоднородная, детально не типизируется; пустой ``dict`` — если сервер вернул
            не-объект.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                params = ImBaseTableSearchParams(table_links_lookup={"204": [1, 2]})
                result = await ips.imbase_attribute_existing_values(
                    "8f3c2a10-0000-0000-0000-000000000000", params
                )
                print(result.get("values", []))

        Notes:
            operationId ``ImBase_GetTableSearchExistingAttributeValues``; путь
            ``POST /core/api/imbase/attribute/byGuid/{attributeGuid}/existingValues``;
            тело — ``ImBaseTableSearchParamsDto``; ответ —
            ``ImBaseTableSearchExistingAttributeValuesDto`` (без result-обёртки).
            См. объектной модели IPS.
        """
        payload = params.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post",
            f"/core/api/imbase/attribute/byGuid/{attribute_guid}/existingValues",
            json=payload,
        )
        return data if isinstance(data, dict) else {}
