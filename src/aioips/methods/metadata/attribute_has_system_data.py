"""Метод проверки наличия системных данных у типа атрибута по id."""

from ...core import APIManager


class AttributeHasSystemDataMixin(APIManager):
    """Реализует ``GET /core/api/metadata/attributeTypes/hasSystemData/{id}``."""

    async def attribute_has_system_data(
        self: "AttributeHasSystemDataMixin",
        attribute_type_id: int,
    ) -> bool:
        """Проверяет, несёт ли тип атрибута системные данные (по id).

        Булев флаг: помечен ли тип атрибута как системный (его данные используются ядром
        IPS, а не только прикладной моделью). Ответ сервера — голое булево значение, без
        обёртки ``...NullableResultDto``.

        Когда применять: чтобы отличить системные атрибуты от прикладных перед
        отображением или редактированием — системные обычно не предназначены для ручной
        правки пользователем. Аналог по GUID — :meth:`attribute_has_system_data_by_guid`.

        Args:
            attribute_type_id: Идентификатор типа атрибута (id-пространство ТИПОВ
                атрибутов метаданных, не значение атрибута объекта).

        Returns:
            ``True`` — тип атрибута несёт системные данные; ``False`` — прикладной атрибут.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                is_system = await ips.attribute_has_system_data(1029)

        Notes:
            operationId ``Metadata_HasAttributeSystemDataById``; путь
            ``GET /core/api/metadata/attributeTypes/hasSystemData/{id}`` (ответ —
            ``boolean``). Аналог по GUID: :meth:`attribute_has_system_data_by_guid`.
        """
        path = f"/core/api/metadata/attributeTypes/hasSystemData/{attribute_type_id}"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
