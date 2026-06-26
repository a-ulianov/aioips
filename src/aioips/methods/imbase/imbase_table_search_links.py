"""Метод получения связей поиска по таблицам справочника для корневого объекта."""

from typing import Any

from ...core import APIManager


class ImBaseTableSearchLinksMixin(APIManager):
    """Реализует ``GET .../links/byParent/{rootObjectId}`` (``ImBase_GetTableSearchLinkList``)."""

    async def imbase_table_search_links(
        self: "ImBaseTableSearchLinksMixin",
        root_object_id: int,
    ) -> list[Any] | None:
        """Возвращает список связей поиска по таблицам справочника для корневого объекта.

        Связь поиска по таблице (``ImBaseTableSearchLinkInfo``) описывает, как от заданного
        корневого объекта искать связанные записи табличных частей справочника. Метод
        отдаёт перечень таких связей для одного корневого объекта. Ответ обёрнут в
        ``...NullableResultDto`` (``{entity, isEntityPresent}``); обёртка разворачивается
        здесь, наружу отдаётся либо список, либо ``None``.

        Когда применять: чтобы определить доступные пути поиска по таблицам справочника от
        конкретного корневого объекта. Предусловий нет (операция чтения).

        Args:
            root_object_id: Идентификатор корневого ОБЪЕКТА (``rootObjectId``, ``ObjectID`` /
                F_OBJECT_ID — общий для версий, не id версии), от которого строятся связи
                поиска.

        Returns:
            Список опаковых элементов как ``list[Any]`` по DTO
            ``ImBaseTableSearchLinkInfoDto``, либо ``None``, если entity отсутствует
            (``isEntityPresent == false``). Элементы неоднородные, детально не
            типизируются; пустой список — связей нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                links = await ips.imbase_table_search_links(102550)  # 102550 = objectID
                if links is not None:
                    for link in links:
                        print(link)

        Notes:
            operationId ``ImBase_GetTableSearchLinkList``; путь
            ``GET /core/api/imbase/links/byParent/{rootObjectId}``
            (``...IEnumerableNullableResultDto`` → entity-массив).
        """
        data = await self._request(
            "get",
            f"/core/api/imbase/links/byParent/{root_object_id}",
        )
        entity = data.get("entity") if isinstance(data, dict) else None
        return list(entity) if isinstance(entity, list) else None
