"""Метод проверки поддержки сортировки типом объекта по GUID."""

from ...core import APIManager


class ObjectTypeHasSortingByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/sorting/objectTypes/byGuid/{guid}/exists``."""

    async def object_type_has_sorting_by_guid(
        self: "ObjectTypeHasSortingByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, поддерживает ли тип объекта сортировку (по GUID).

        Возвращает ``True``, если у типа объекта есть сортирующие типы связей, то есть
        порядок экземпляров (потомков) можно задавать. GUID типа объекта стабилен между
        установками IPS (в отличие от ``id``). Ответ сервера — голое булево значение,
        без обёртки ``...NullableResultDto``.

        Когда применять: переносимая проверка поддержки сортировки типом по стабильному
        GUID (сверка конфигурации между средами). Аналог по id —
        :meth:`object_type_has_sorting`.

        Args:
            guid: GUID ТИПА объекта (стабильный идентификатор типа), строка вида
                ``cad001c5-306c-11d8-b4e9-00304f19f545``.

        Returns:
            ``True`` — у типа есть сортирующие типы связей; ``False`` — нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ok = await ips.object_type_has_sorting_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_HasObjectTypeSortingRelationTypesByGuid``; путь
            ``GET /core/api/metadata/sorting/objectTypes/byGuid/{guid}/exists`` (ответ —
            ``boolean``). Связанный метод: :meth:`object_type_has_sorting`.
        """
        path = f"/core/api/metadata/sorting/objectTypes/byGuid/{guid}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
