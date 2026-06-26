"""Метод проверки наличия замещающих связей у типа объекта по GUID."""

from urllib.parse import quote

from ...core import APIManager


class ObjectTypeHasSubstitutionByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/substitution/objectTypes/byGuid/{guid}/exists``."""

    async def object_type_has_substitution_by_guid(
        self: "ObjectTypeHasSubstitutionByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, есть ли у типа объекта замещающие типы связей (по GUID).

        Замещение — механизм IPS, в котором один объект замещает другой через специальные
        связи замещения. Метод отвечает, определены ли для типа объекта с данным ``guid``
        типы связей замещения. GUID типа объекта стабилен между установками IPS (в отличие
        от ``id``). Ответ сервера — голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: переносимый (по стабильному GUID) предварительный фильтр перед
        обходом связей замещения у объектов данного типа. Аналог по id —
        :meth:`object_type_has_substitution`.

        Args:
            guid: GUID типа объекта (стабильный идентификатор типа), строка вида
                ``"11111111-2222-3333-4444-555555555555"``. Кодируется в URL.

        Returns:
            ``True`` — у типа объекта есть замещающие типы связей; ``False`` — нет
            (в том числе если сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = "11111111-2222-3333-4444-555555555555"
                flag = await ips.object_type_has_substitution_by_guid(guid)

        Notes:
            operationId ``Metadata_HasObjectTypeSubstituteRelationTypesByGuid``; путь
            ``GET /core/api/metadata/substitution/objectTypes/byGuid/{guid}/exists``
            (ответ — ``boolean``). Связанный метод: :meth:`object_type_has_substitution`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/substitution/objectTypes/byGuid/{encoded_guid}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
