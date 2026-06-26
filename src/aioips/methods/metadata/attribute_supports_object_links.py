"""Метод проверки поддержки ссылок на объекты системным атрибутом (по GUID)."""

from ...core import APIManager


class AttributeSupportsObjectLinksMixin(APIManager):
    """Реализует ``GET /core/api/metadata/attributeTypes/supportsObjectLinks/byGuid/{guid}``."""

    async def attribute_supports_object_links(
        self: "AttributeSupportsObjectLinksMixin",
        guid: str,
    ) -> bool:
        """Проверяет, поддерживает ли системный тип атрибута ссылки на объекты (по GUID).

        Булев флаг: может ли значение системного атрибута быть ссылкой на объект
        (``ftObjectLink``) — например, атрибут-ссылка вроде «Архив». GUID типа атрибута
        стабилен между установками IPS. Ответ сервера — голое булево значение, без обёртки
        ``...NullableResultDto``.

        Когда применять: чтобы перед чтением значения как ссылки убедиться, что системный
        атрибут вообще поддерживает связь с объектом (иначе значение трактуется иначе).
        Тип данных целиком виден в :meth:`attribute_type_by_guid` (поле ``field_type``).
        См. объектной модели IPS (атрибут-ссылка ``ftObjectLink``).

        Args:
            guid: GUID типа атрибута (стабильный идентификатор типа в id-пространстве
                ТИПОВ атрибутов), строка вида ``cad001c5-306c-11d8-b4e9-00304f19f545``.

        Returns:
            ``True`` — системный атрибут поддерживает ссылки на объекты; ``False`` — нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                supports = await ips.attribute_supports_object_links(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_IsSystemAttributeSupportsObjectLinks``; путь
            ``GET /core/api/metadata/attributeTypes/supportsObjectLinks/byGuid/{guid}``
            (ответ — ``boolean``). Связанный метод: :meth:`attribute_type_by_guid`.
        """
        path = f"/core/api/metadata/attributeTypes/supportsObjectLinks/byGuid/{guid}"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
