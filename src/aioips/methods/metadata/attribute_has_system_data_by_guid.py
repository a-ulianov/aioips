"""Метод проверки наличия системных данных у типа атрибута по GUID."""

from ...core import APIManager


class AttributeHasSystemDataByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/attributeTypes/hasSystemData/byGuid/{guid}``."""

    async def attribute_has_system_data_by_guid(
        self: "AttributeHasSystemDataByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, несёт ли тип атрибута системные данные (по GUID).

        Булев флаг: помечен ли тип атрибута как системный (его данные используются ядром
        IPS, а не только прикладной моделью). GUID типа атрибута стабилен между установками
        IPS. Ответ сервера — голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: чтобы по стабильному GUID отличить системный атрибут от
        прикладного перед отображением или редактированием — системные обычно не
        предназначены для ручной правки. Аналог по id — :meth:`attribute_has_system_data`.

        Args:
            guid: GUID типа атрибута (стабильный идентификатор типа в id-пространстве
                ТИПОВ атрибутов), строка вида ``cad001c5-306c-11d8-b4e9-00304f19f545``.

        Returns:
            ``True`` — тип атрибута несёт системные данные; ``False`` — прикладной атрибут.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                is_system = await ips.attribute_has_system_data_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_HasAttributeSystemDataByGuid``; путь
            ``GET /core/api/metadata/attributeTypes/hasSystemData/byGuid/{guid}`` (ответ —
            ``boolean``). Аналог по id: :meth:`attribute_has_system_data`.
        """
        path = f"/core/api/metadata/attributeTypes/hasSystemData/byGuid/{guid}"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
