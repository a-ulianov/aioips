"""Метод проверки наличия замещений у типа связи по id."""

from ...core import APIManager


class RelationTypeHasSubstitutesMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/substitution/relationTypes/{id}/exists``."""

    async def relation_type_has_substitutes(
        self: "RelationTypeHasSubstitutesMixin",
        id: int,
    ) -> bool:
        """Проверяет, поддерживает ли тип связи замещения (по id).

        Замещение реализуется через специальные типы связей. Метод отвечает, является ли
        тип связи с данным ``id`` тем, через который выражается замещение (то есть могут ли
        связи этого типа задавать замещение объектов). Ответ сервера — голое булево
        значение, без обёртки ``...NullableResultDto``.

        Когда применять: как дешёвый предварительный фильтр при разборе связей объекта —
        чтобы отличить связи замещения от прочих. Аналог по GUID —
        :meth:`relation_type_has_substitutes_by_guid`; перечень всех таких типов —
        :meth:`substitute_relation_type_ids`.

        Args:
            id: Идентификатор типа связи (id-пространство ТИПОВ связей метаданных,
                не id конкретной связи ``RelationID``).

        Returns:
            ``True`` — тип связи поддерживает замещения; ``False`` — нет (в том числе если
            сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.relation_type_has_substitutes(7):
                    print("связи этого типа задают замещение")

        Notes:
            operationId ``Metadata_HasRelationTypeSubstitutesById``; путь
            ``GET /core/api/metadata/substitution/relationTypes/{id}/exists`` (ответ —
            ``boolean``). Связанные методы: :meth:`relation_type_has_substitutes_by_guid`,
            :meth:`substitute_relation_type_ids`.
        """
        path = f"/core/api/metadata/substitution/relationTypes/{id}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
