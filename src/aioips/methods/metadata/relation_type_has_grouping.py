"""Метод проверки участия типа связи в группировке по id."""

from ...core import APIManager


class RelationTypeHasGroupingMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/grouping/relationTypes/{id}/exists``."""

    async def relation_type_has_grouping(
        self: "RelationTypeHasGroupingMixin",
        relation_type_id: int,
    ) -> bool:
        """Проверяет, участвует ли тип связи в группировке (по id).

        Возвращает ``True``, если тип связи помечен как группирующий, то есть по нему
        выполняется группировка экземпляров. Дополняет проверки на уровне типов объектов
        (:meth:`object_type_has_grouping`), но в пространстве типов СВЯЗЕЙ. Ответ сервера —
        голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: как дешёвый фильтр перед операциями группировки по конкретному
        типу связи. Аналог по GUID — :meth:`relation_type_has_grouping_by_guid`; полный
        перечень — :meth:`grouping_relation_type_ids`.

        Args:
            relation_type_id: Идентификатор ТИПА связи (id-пространство типов связей
                метаданных, не id конкретной связи ``RelationID``).

        Returns:
            ``True`` — тип связи участвует в группировке; ``False`` — нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ok = await ips.relation_type_has_grouping(7)

        Notes:
            operationId ``Metadata_HasRelationTypeGroupingById``; путь
            ``GET /core/api/metadata/grouping/relationTypes/{id}/exists`` (ответ —
            ``boolean``). Связанные методы: :meth:`relation_type_has_grouping_by_guid`,
            :meth:`grouping_relation_type_ids`.
        """
        path = f"/core/api/metadata/grouping/relationTypes/{relation_type_id}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
