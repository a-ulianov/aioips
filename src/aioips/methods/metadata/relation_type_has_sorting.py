"""Метод проверки участия типа связи в сортировке по id."""

from ...core import APIManager


class RelationTypeHasSortingMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/sorting/relationTypes/{id}/exists``."""

    async def relation_type_has_sorting(
        self: "RelationTypeHasSortingMixin",
        relation_type_id: int,
    ) -> bool:
        """Проверяет, участвует ли тип связи в сортировке (по id).

        Возвращает ``True``, если тип связи помечен как сортирующий, то есть по нему
        задаётся порядок экземпляров. Дополняет проверки на уровне типов объектов
        (:meth:`object_type_has_sorting`), но в пространстве типов СВЯЗЕЙ. Ответ сервера —
        голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: как дешёвый фильтр перед операциями упорядочивания по конкретному
        типу связи. Аналог по GUID — :meth:`relation_type_has_sorting_by_guid`; полный
        перечень — :meth:`sorting_relation_type_ids`.

        Args:
            relation_type_id: Идентификатор ТИПА связи (id-пространство типов связей
                метаданных, не id конкретной связи ``RelationID``).

        Returns:
            ``True`` — тип связи участвует в сортировке; ``False`` — нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ok = await ips.relation_type_has_sorting(7)

        Notes:
            operationId ``Metadata_HasRelationTypeSortingById``; путь
            ``GET /core/api/metadata/sorting/relationTypes/{id}/exists`` (ответ —
            ``boolean``). Связанные методы: :meth:`relation_type_has_sorting_by_guid`,
            :meth:`sorting_relation_type_ids`.
        """
        path = f"/core/api/metadata/sorting/relationTypes/{relation_type_id}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
