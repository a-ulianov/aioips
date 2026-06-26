"""Метод проверки участия типа связи в группировке по GUID."""

from ...core import APIManager


class RelationTypeHasGroupingByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/grouping/relationTypes/{guid}/exists``."""

    async def relation_type_has_grouping_by_guid(
        self: "RelationTypeHasGroupingByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, участвует ли тип связи в группировке (по GUID).

        Возвращает ``True``, если тип связи помечен как группирующий, то есть по нему
        выполняется группировка экземпляров. GUID типа связи стабилен между установками
        IPS (в отличие от ``id``), поэтому пригоден для переносимых проверок. Ответ
        сервера — голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: переносимая проверка участия типа связи в группировке по
        стабильному GUID (сверка конфигурации между средами). Аналог по id —
        :meth:`relation_type_has_grouping`.

        Args:
            guid: GUID ТИПА связи (стабильный идентификатор типа связи), строка вида
                ``cad001c5-306c-11d8-b4e9-00304f19f545``.

        Returns:
            ``True`` — тип связи участвует в группировке; ``False`` — нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ok = await ips.relation_type_has_grouping_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_HasRelationTypeGroupingByGuid``; путь
            ``GET /core/api/metadata/grouping/relationTypes/{guid}/exists`` (ответ —
            ``boolean``). Связанный метод: :meth:`relation_type_has_grouping`.
        """
        path = f"/core/api/metadata/grouping/relationTypes/{guid}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
