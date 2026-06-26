"""Метод проверки наличия проектируемой связи у типа объекта по GUID."""

from urllib.parse import quote

from ...core import APIManager


class ObjectTypeHasDesignByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/design/objectTypes/byGuid/{guid}/exists``."""

    async def object_type_has_design_by_guid(
        self: "ObjectTypeHasDesignByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, есть ли у типа объекта проектируемый тип связи (по GUID).

        Возвращает ``True``, если для типа объекта задан хотя бы один проектируемый
        (designed) тип связи, то есть состав потомков такого типа можно проектировать.
        GUID типа объекта стабилен между установками IPS (в отличие от ``id``). Ответ
        сервера — голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: переносимая проверка наличия проектируемой связи по стабильному
        GUID (сверка конфигурации между средами). Аналог по id —
        :meth:`object_type_has_design`.

        Args:
            guid: GUID ТИПА объекта (стабильный идентификатор типа), строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``. Кодируется в URL.

        Returns:
            ``True`` — у типа есть проектируемый тип связи; ``False`` — нет (в том числе
            если сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ok = await ips.object_type_has_design_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_HasObjectTypeDesignedRelationTypeByGuid``; путь
            ``GET /core/api/metadata/design/objectTypes/byGuid/{guid}/exists`` (ответ —
            ``boolean``). Аналог по id: :meth:`object_type_has_design`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/design/objectTypes/byGuid/{encoded_guid}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
