"""Метод проверки наличия замещений у типа связи по GUID."""

from urllib.parse import quote

from ...core import APIManager


class RelationTypeHasSubstitutesByGuidMixin(APIManager):
    """Реализует ``GET .../substitution/relationTypes/byGuid/{guid}/exists``."""

    async def relation_type_has_substitutes_by_guid(
        self: "RelationTypeHasSubstitutesByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, поддерживает ли тип связи замещения (по GUID).

        Замещение реализуется через специальные типы связей. Метод отвечает, является ли
        тип связи с данным ``guid`` тем, через который выражается замещение. GUID типа связи
        стабилен между установками IPS (в отличие от ``id``). Ответ сервера — голое булево
        значение, без обёртки ``...NullableResultDto``.

        Когда применять: переносимый (по стабильному GUID) предварительный фильтр при
        разборе связей объекта — чтобы отличить связи замещения от прочих. Аналог по id —
        :meth:`relation_type_has_substitutes`.

        Args:
            guid: GUID типа связи (стабильный идентификатор типа связи), строка вида
                ``"11111111-2222-3333-4444-555555555555"``. Кодируется в URL.

        Returns:
            ``True`` — тип связи поддерживает замещения; ``False`` — нет (в том числе если
            сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = "11111111-2222-3333-4444-555555555555"
                flag = await ips.relation_type_has_substitutes_by_guid(guid)

        Notes:
            operationId ``Metadata_HasRelationTypeSubstitutesByGuid``; путь
            ``GET /core/api/metadata/substitution/relationTypes/byGuid/{guid}/exists``
            (ответ — ``boolean``). Связанный метод: :meth:`relation_type_has_substitutes`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/substitution/relationTypes/byGuid/{encoded_guid}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
