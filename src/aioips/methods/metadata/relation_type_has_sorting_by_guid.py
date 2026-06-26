"""Метод проверки участия типа связи в сортировке по GUID."""

from ...core import APIManager


class RelationTypeHasSortingByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/sorting/relationTypes/byGuid/{guid}/exists``."""

    async def relation_type_has_sorting_by_guid(
        self: "RelationTypeHasSortingByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, участвует ли тип связи в сортировке (по GUID).

        Возвращает ``True``, если тип связи помечен как сортирующий, то есть по нему
        задаётся порядок экземпляров. GUID типа связи стабилен между установками IPS
        (в отличие от ``id``), поэтому пригоден для переносимых проверок. Ответ сервера —
        голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: переносимая проверка участия типа связи в сортировке по
        стабильному GUID (сверка конфигурации между средами). Аналог по id —
        :meth:`relation_type_has_sorting`.

        Args:
            guid: GUID ТИПА связи (стабильный идентификатор типа связи), строка вида
                ``cad001c5-306c-11d8-b4e9-00304f19f545``.

        Returns:
            ``True`` — тип связи участвует в сортировке; ``False`` — нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ok = await ips.relation_type_has_sorting_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_HasRelationTypeSortingByGuid``; путь
            ``GET /core/api/metadata/sorting/relationTypes/byGuid/{guid}/exists`` (ответ —
            ``boolean``). Связанный метод: :meth:`relation_type_has_sorting`.
        """
        path = f"/core/api/metadata/sorting/relationTypes/byGuid/{guid}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
