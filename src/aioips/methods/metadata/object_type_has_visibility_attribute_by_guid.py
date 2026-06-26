"""Метод проверки наличия атрибута видимости у типа объекта по GUID."""

from urllib.parse import quote

from ...core import APIManager


class ObjectTypeHasVisibilityAttributeByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/visibility/objectTypes/byGuid/{guid}/exists``."""

    async def object_type_has_visibility_attribute_by_guid(
        self: "ObjectTypeHasVisibilityAttributeByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, есть ли у типа объекта атрибут видимости (по GUID).

        Возвращает ``True``, если у типа объекта задан атрибут видимости (visibility) —
        то есть видимость его экземпляров управляется специальным атрибутом. GUID типа
        объекта стабилен между установками IPS (в отличие от ``id``). Ответ сервера —
        голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: переносимая проверка наличия атрибута видимости по стабильному
        GUID (сверка конфигурации между средами). Аналог по id —
        :meth:`object_type_has_visibility_attribute`.

        Args:
            guid: GUID ТИПА объекта (стабильный идентификатор типа), строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``. Кодируется в URL.

        Returns:
            ``True`` — у типа есть атрибут видимости; ``False`` — нет (в том числе если
            сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ok = await ips.object_type_has_visibility_attribute_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_HasObjectTypeVisibilityAttributeByGuid``; путь
            ``GET /core/api/metadata/visibility/objectTypes/byGuid/{guid}/exists`` (ответ —
            ``boolean``). Аналог по id: :meth:`object_type_has_visibility_attribute`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/visibility/objectTypes/byGuid/{encoded_guid}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
