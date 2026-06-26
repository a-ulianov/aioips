"""Метод проверки наличия списка допустимых значений у атрибута по id."""

from ...core import APIManager


class AttributeHasPossibleValuesMixin(APIManager):
    """Реализует ``GET /core/api/metadata/attributeTypes/hasPossibleValues/{id}``."""

    async def attribute_has_possible_values(
        self: "AttributeHasPossibleValuesMixin",
        attribute_type_id: int,
    ) -> bool:
        """Проверяет, задан ли у типа атрибута список допустимых значений (по id).

        Булев флаг: ограничен ли атрибут заранее заданным перечнем значений (атрибут «из
        списка»). Ответ сервера — голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: чтобы перед чтением/редактированием значения понять, нужно ли
        выбирать его из перечня ``possible_values`` (а не вводить произвольно) — например,
        для построения выпадающего списка в UI. Полный перечень значений и метаописание —
        в :meth:`attribute_type` (поле ``possible_values``). Аналог по GUID —
        :meth:`attribute_has_possible_values_by_guid`.

        Args:
            attribute_type_id: Идентификатор типа атрибута (id-пространство ТИПОВ
                атрибутов метаданных, не значение атрибута объекта).

        Returns:
            ``True`` — у типа атрибута задан список допустимых значений; ``False`` —
            значение свободное (перечня нет).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.attribute_has_possible_values(1029):
                    attr = await ips.attribute_type(1029)

        Notes:
            operationId ``Metadata_HasAttributePossibleValuesById``; путь
            ``GET /core/api/metadata/attributeTypes/hasPossibleValues/{id}`` (ответ —
            ``boolean``). Связанные методы: :meth:`attribute_type`,
            :meth:`attribute_has_possible_values_by_guid`.
        """
        path = f"/core/api/metadata/attributeTypes/hasPossibleValues/{attribute_type_id}"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
