"""Метод проверки пригодности типа атрибута для отображения в таблице (по id)."""

from ...core import APIManager


class AttributeIsGridableMixin(APIManager):
    """Реализует ``GET /core/api/metadata/attributeTypes/isGridable/{id}``."""

    async def attribute_is_gridable(
        self: "AttributeIsGridableMixin",
        attribute_type_id: int,
    ) -> bool:
        """Проверяет, можно ли выводить тип атрибута колонкой таблицы (по id).

        Булев флаг: пригоден ли атрибут для отображения в табличном представлении
        (gridable) — то есть может ли он быть колонкой грида. Ответ сервера — голое булево
        значение, без обёртки ``...NullableResultDto``.

        Когда применять: при построении табличных представлений/отчётов — чтобы
        отфильтровать атрибуты, непригодные для вывода колонкой (например, тяжёлые или
        неотображаемые типы). Аналог по GUID — :meth:`attribute_is_gridable_by_guid`.

        Args:
            attribute_type_id: Идентификатор типа атрибута (id-пространство ТИПОВ
                атрибутов метаданных, не значение атрибута объекта).

        Returns:
            ``True`` — атрибут можно вывести колонкой таблицы; ``False`` — непригоден для
            табличного отображения.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.attribute_is_gridable(1029):
                    ...  # добавить колонку в грид

        Notes:
            operationId ``Metadata_IsAttributeGridableById``; путь
            ``GET /core/api/metadata/attributeTypes/isGridable/{id}`` (ответ — ``boolean``).
            Аналог по GUID: :meth:`attribute_is_gridable_by_guid`.
        """
        path = f"/core/api/metadata/attributeTypes/isGridable/{attribute_type_id}"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
