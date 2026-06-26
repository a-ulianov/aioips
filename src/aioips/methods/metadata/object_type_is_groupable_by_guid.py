"""Метод проверки группируемости типа объекта по GUID."""

from ...core import APIManager


class ObjectTypeIsGroupableByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/grouping/objectTypes/groupable/byGuid/{guid}/exists``."""

    async def object_type_is_groupable_by_guid(
        self: "ObjectTypeIsGroupableByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, можно ли группировать экземпляры типа объекта (по GUID).

        «Groupable» означает, что экземпляры типа могут быть СГРУППИРОВАНЫ (выступать
        сгруппированными потомками) через сгруппированные типы связей, в отличие от
        «grouping» (тип сам выполняет группировку, см.
        :meth:`object_type_has_grouping_by_guid`). GUID типа объекта стабилен между
        установками IPS (в отличие от ``id``). Ответ сервера — голое булево значение,
        без обёртки ``...NullableResultDto``.

        Когда применять: переносимая проверка группируемости типа по стабильному GUID
        (сверка конфигурации между средами). Аналог по id — :meth:`object_type_is_groupable`.

        Args:
            guid: GUID ТИПА объекта (стабильный идентификатор типа), строка вида
                ``cad001c5-306c-11d8-b4e9-00304f19f545``.

        Returns:
            ``True`` — у типа есть сгруппированные типы связей (экземпляры группируемы);
            ``False`` — нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ok = await ips.object_type_is_groupable_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_HasObjectTypeGroupedRelationTypesByGuid``; путь
            ``GET /core/api/metadata/grouping/objectTypes/groupable/byGuid/{guid}/exists``
            (ответ — ``boolean``). Связанный метод: :meth:`object_type_is_groupable`.
        """
        path = f"/core/api/metadata/grouping/objectTypes/groupable/byGuid/{guid}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
