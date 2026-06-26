"""Метод проверки наличия списка допустимых значений у атрибута по GUID."""

from ...core import APIManager


class AttributeHasPossibleValuesByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/attributeTypes/hasPossibleValues/byGuid/{guid}``."""

    async def attribute_has_possible_values_by_guid(
        self: "AttributeHasPossibleValuesByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, задан ли у типа атрибута список допустимых значений (по GUID).

        Булев флаг: ограничен ли атрибут заранее заданным перечнем значений (атрибут «из
        списка»). GUID типа атрибута стабилен между установками IPS. Ответ сервера — голое
        булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: чтобы по стабильному GUID понять, нужно ли выбирать значение из
        перечня ``possible_values`` (а не вводить произвольно) — например, при построении
        UI по переносимой конфигурации. Полный перечень — в :meth:`attribute_type_by_guid`.
        Аналог по id — :meth:`attribute_has_possible_values`.

        Args:
            guid: GUID типа атрибута (стабильный идентификатор типа в id-пространстве
                ТИПОВ атрибутов), строка вида ``cad001c5-306c-11d8-b4e9-00304f19f545``.

        Returns:
            ``True`` — у типа атрибута задан список допустимых значений; ``False`` —
            значение свободное (перечня нет).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                has_values = await ips.attribute_has_possible_values_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_HasAttributePossibleValuesByGuid``; путь
            ``GET /core/api/metadata/attributeTypes/hasPossibleValues/byGuid/{guid}``
            (ответ — ``boolean``). Связанные методы: :meth:`attribute_type_by_guid`,
            :meth:`attribute_has_possible_values`.
        """
        path = f"/core/api/metadata/attributeTypes/hasPossibleValues/byGuid/{guid}"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
