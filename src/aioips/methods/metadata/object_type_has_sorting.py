"""Метод проверки поддержки сортировки типом объекта по id."""

from ...core import APIManager


class ObjectTypeHasSortingMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/sorting/objectTypes/{id}/exists``."""

    async def object_type_has_sorting(
        self: "ObjectTypeHasSortingMixin",
        object_type_id: int,
    ) -> bool:
        """Проверяет, поддерживает ли тип объекта сортировку (по id).

        Возвращает ``True``, если у типа объекта есть сортирующие типы связей, то есть
        порядок экземпляров (потомков) можно задавать. Ответ сервера — голое булево
        значение, без обёртки ``...NullableResultDto``.

        Когда применять: как дешёвый фильтр перед операциями упорядочивания экземпляров
        данного типа. Аналог по GUID — :meth:`object_type_has_sorting_by_guid`; полный
        перечень типов с сортировкой — :meth:`sorting_object_type_ids`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (id-пространство типов объектов
                метаданных, не id объекта/версии).

        Returns:
            ``True`` — у типа есть сортирующие типы связей; ``False`` — нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.object_type_has_sorting(42):
                    rels = await ips.sorting_relation_type_ids()

        Notes:
            operationId ``Metadata_HasObjectTypeSortingRelationTypesById``; путь
            ``GET /core/api/metadata/sorting/objectTypes/{id}/exists`` (ответ —
            ``boolean``). Связанные методы: :meth:`object_type_has_sorting_by_guid`,
            :meth:`sorting_object_type_ids`.
        """
        path = f"/core/api/metadata/sorting/objectTypes/{object_type_id}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
