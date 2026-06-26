"""Метод проверки существования типа связи по идентификатору."""

from ...core import APIManager


class RelationTypeMetaExistsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/relationTypes/{id}/exists``."""

    async def relation_type_meta_exists(
        self: "RelationTypeMetaExistsMixin",
        relation_type_id: int,
    ) -> bool:
        """Проверяет, существует ли тип связи с заданным идентификатором.

        Дешёвый булев флаг наличия типа связи в метамодели — без загрузки полного
        описания. Ответ сервера — голое булево значение, без обёртки
        ``...NullableResultDto``.

        Когда применять: как предварительная валидация ``id`` типа связи перед
        вызовами раздела ``relation_types``/``relation_queries`` или перед
        :meth:`relation_type_meta`, чтобы отличить отсутствие типа от прочих ошибок.

        Args:
            relation_type_id: Идентификатор типа связи (``RelationType`` —
                id-пространство ТИПОВ связей, не ``RelationID`` конкретной связи).

        Returns:
            ``True`` — тип связи с таким id существует; ``False`` — не существует.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.relation_type_meta_exists(501):
                    rel = await ips.relation_type_meta(501)

        Notes:
            operationId ``Metadata_ExistsRelationTypeById``; путь
            ``GET /core/api/metadata/relationTypes/{id}/exists`` (ответ — ``boolean``).
            Аналог по GUID — :meth:`relation_type_meta_exists_by_guid`.
        """
        path = f"/core/api/metadata/relationTypes/{relation_type_id}/exists"
        data = await self._request("get", path)
        return bool(data)
