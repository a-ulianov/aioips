"""Метод проверки наличия группировки у типа объекта по id."""

from ...core import APIManager


class ObjectTypeHasGroupingMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/grouping/objectTypes/grouping/{id}/exists``."""

    async def object_type_has_grouping(
        self: "ObjectTypeHasGroupingMixin",
        object_type_id: int,
    ) -> bool:
        """Проверяет, выполняет ли тип объекта группировку (по id).

        Возвращает ``True``, если у типа объекта есть группирующие типы связей, то есть
        тип сам ВЫПОЛНЯЕТ группировку (группирующий родитель), в отличие от «groupable»
        (тип может быть сгруппирован, см. :meth:`object_type_is_groupable`). Ответ
        сервера — голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: как дешёвый фильтр перед операциями группировки потомков данного
        типа. Аналог по GUID — :meth:`object_type_has_grouping_by_guid`; полный перечень
        типов-группировщиков — :meth:`grouping_object_type_ids`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (id-пространство типов объектов
                метаданных, не id объекта/версии).

        Returns:
            ``True`` — у типа есть группирующие типы связей; ``False`` — нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.object_type_has_grouping(42):
                    rels = await ips.grouping_relation_type_ids()

        Notes:
            operationId ``Metadata_HasObjectTypeGroupingRelationTypesById``; путь
            ``GET /core/api/metadata/grouping/objectTypes/grouping/{id}/exists`` (ответ —
            ``boolean``). Связанные методы: :meth:`object_type_has_grouping_by_guid`,
            :meth:`grouping_object_type_ids`, :meth:`object_type_is_groupable`.
        """
        path = f"/core/api/metadata/grouping/objectTypes/grouping/{object_type_id}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
