"""Метод проверки наличия группировки у типа объекта по GUID."""

from ...core import APIManager


class ObjectTypeHasGroupingByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/grouping/objectTypes/grouping/byGuid/{guid}/exists``."""

    async def object_type_has_grouping_by_guid(
        self: "ObjectTypeHasGroupingByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, выполняет ли тип объекта группировку (по GUID).

        Возвращает ``True``, если у типа объекта есть группирующие типы связей, то есть
        тип сам ВЫПОЛНЯЕТ группировку (группирующий родитель), в отличие от «groupable»
        (тип может быть сгруппирован, см. :meth:`object_type_is_groupable_by_guid`). GUID
        типа объекта стабилен между установками IPS (в отличие от ``id``). Ответ сервера —
        голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: переносимая проверка наличия группировки у типа по стабильному
        GUID (сверка конфигурации между средами). Аналог по id —
        :meth:`object_type_has_grouping`.

        Args:
            guid: GUID ТИПА объекта (стабильный идентификатор типа), строка вида
                ``cad001c5-306c-11d8-b4e9-00304f19f545``.

        Returns:
            ``True`` — у типа есть группирующие типы связей; ``False`` — нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ok = await ips.object_type_has_grouping_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_HasObjectTypeGroupingRelationTypesByGuid``; путь
            ``GET /core/api/metadata/grouping/objectTypes/grouping/byGuid/{guid}/exists``
            (ответ — ``boolean``). Связанный метод: :meth:`object_type_has_grouping`.
        """
        path = f"/core/api/metadata/grouping/objectTypes/grouping/byGuid/{guid}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
