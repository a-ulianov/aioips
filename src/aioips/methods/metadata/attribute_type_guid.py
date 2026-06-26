"""Метод получения GUID типа атрибута по идентификатору."""

from ...core import APIManager


class AttributeTypeGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeTypes/{id}/guid``."""

    async def attribute_type_guid(
        self: "AttributeTypeGuidMixin",
        attribute_type_id: int,
    ) -> str:
        """Возвращает GUID типа атрибута по его идентификатору.

        Мост «id → GUID»: переводит локальный числовой ``id`` типа атрибута в стабильный
        GUID, переносимый между установками IPS. Ответ сервера — строка (GUID), а не
        объект-обёртка.

        Когда применять: чтобы сохранить переносимую ссылку на тип атрибута (для сверки
        конфигурации между средами) по известному ``id`` текущей среды. Обратное
        направление — :meth:`attribute_type_id_by_guid`; аналог по имени —
        :meth:`attribute_type_guid_by_name`.

        Args:
            attribute_type_id: Идентификатор типа атрибута (id-пространство ТИПОВ
                атрибутов метаданных, не значение атрибута объекта).

        Returns:
            GUID типа атрибута как строка. Пустая строка, если сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если тип атрибута с таким
                ``id`` не найден).

        Example:
            async with IPSClient(config=config) as ips:
                guid = await ips.attribute_type_guid(1029)

        Notes:
            operationId ``Metadata_GetAttributeTypeGuid``; путь
            ``GET /core/api/metadata/attributeTypes/{id}/guid``. Связанные методы:
            :meth:`attribute_type_id_by_guid`, :meth:`attribute_type_guid_by_name`.
        """
        path = f"/core/api/metadata/attributeTypes/{attribute_type_id}/guid"
        data = await self._request("get", path)
        return "" if data is None else str(data)
