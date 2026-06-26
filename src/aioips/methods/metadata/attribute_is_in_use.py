"""Метод проверки использования типа атрибута по id."""

from ...core import APIManager


class AttributeIsInUseMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeTypeApplicability/{id}/inUse``."""

    async def attribute_is_in_use(
        self: "AttributeIsInUseMixin",
        attribute_type_id: int,
    ) -> bool:
        """Проверяет, используется ли тип атрибута где-либо (по id).

        Дешёвый булев предикат поверх применимости: ``True`` означает, что тип атрибута
        задействован у объектов или связей (применимость не ``none``). В отличие от
        :meth:`attribute_type_applicability` (возвращает конкретную категорию), здесь
        отдаётся только факт использования. Ответ сервера — голое булево значение, без
        обёртки ``...NullableResultDto``.

        Когда применять: как быстрый фильтр перед удалением/изменением типа атрибута —
        чтобы не трогать задействованные типы. Точная категория — через
        :meth:`attribute_type_applicability`; аналог по GUID — :meth:`attribute_is_in_use_by_guid`.

        Args:
            attribute_type_id: Идентификатор ТИПА атрибута (id-пространство типов
                атрибутов метаданных, не значение атрибута объекта).

        Returns:
            ``True`` — тип атрибута используется (применим к объектам или связям);
            ``False`` — не используется нигде.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.attribute_is_in_use(1029):
                    kind = await ips.attribute_type_applicability(1029)

        Notes:
            operationId ``Metadata_IsAttributeInUseById``; путь
            ``GET /core/api/metadata/attributeTypeApplicability/{id}/inUse`` (ответ —
            ``boolean``). Связанные методы: :meth:`attribute_type_applicability`,
            :meth:`attribute_is_in_use_by_guid`.
        """
        path = f"/core/api/metadata/attributeTypeApplicability/{attribute_type_id}/inUse"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
