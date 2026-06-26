"""Метод проверки существования типа атрибута по GUID."""

from ...core import APIManager


class AttributeTypeExistsByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeTypes/byGuid/{guid}/exists``."""

    async def attribute_type_exists_by_guid(
        self: "AttributeTypeExistsByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет существование типа атрибута по его GUID.

        Быстрый булев флаг: зарегистрирован ли в метаданных тип атрибута с заданным
        ``guid``. GUID типа атрибута стабилен между установками IPS (в отличие от ``id``),
        поэтому пригоден для переносимых проверок. Ответ сервера — голое булево значение,
        без обёртки ``...NullableResultDto``.

        Когда применять: как дешёвый предварительный фильтр перед запросом метаописания
        по GUID (:meth:`attribute_type_by_guid`) — например, при сверке конфигурации
        между средами по стабильному GUID. Аналог по id — :meth:`attribute_type_exists`.

        Args:
            guid: GUID типа атрибута (стабильный идентификатор типа в id-пространстве
                ТИПОВ атрибутов), строка вида ``cad001c5-306c-11d8-b4e9-00304f19f545``.

        Returns:
            ``True`` — тип атрибута с таким ``guid`` существует; ``False`` — не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                exists = await ips.attribute_type_exists_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_ExistsAttributeTypeByGuid``; путь
            ``GET /core/api/metadata/attributeTypes/byGuid/{guid}/exists`` (ответ —
            ``boolean``). Связанный метод: :meth:`attribute_type_by_guid`.
        """
        path = f"/core/api/metadata/attributeTypes/byGuid/{guid}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
