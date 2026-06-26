"""Метод проверки пригодности типа атрибута для отображения в таблице (по GUID)."""

from ...core import APIManager


class AttributeIsGridableByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/attributeTypes/isGridable/byGuid/{guid}``."""

    async def attribute_is_gridable_by_guid(
        self: "AttributeIsGridableByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, можно ли выводить тип атрибута колонкой таблицы (по GUID).

        Булев флаг: пригоден ли атрибут для отображения в табличном представлении
        (gridable) — то есть может ли он быть колонкой грида. GUID типа атрибута стабилен
        между установками IPS. Ответ сервера — голое булево значение, без обёртки
        ``...NullableResultDto``.

        Когда применять: при построении табличных представлений/отчётов по переносимой
        конфигурации (стабильный GUID) — чтобы отфильтровать атрибуты, непригодные для
        вывода колонкой. Аналог по id — :meth:`attribute_is_gridable`.

        Args:
            guid: GUID типа атрибута (стабильный идентификатор типа в id-пространстве
                ТИПОВ атрибутов), строка вида ``cad001c5-306c-11d8-b4e9-00304f19f545``.

        Returns:
            ``True`` — атрибут можно вывести колонкой таблицы; ``False`` — непригоден для
            табличного отображения.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                gridable = await ips.attribute_is_gridable_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_IsAttributeGridableByGuid``; путь
            ``GET /core/api/metadata/attributeTypes/isGridable/byGuid/{guid}`` (ответ —
            ``boolean``). Аналог по id: :meth:`attribute_is_gridable`.
        """
        path = f"/core/api/metadata/attributeTypes/isGridable/byGuid/{guid}"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
