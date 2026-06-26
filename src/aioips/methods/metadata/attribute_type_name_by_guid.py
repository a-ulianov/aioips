"""Метод получения имени типа атрибута по GUID."""

from ...core import APIManager


class AttributeTypeNameByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeTypes/byGuid/{guid}/name``."""

    async def attribute_type_name_by_guid(
        self: "AttributeTypeNameByGuidMixin",
        guid: str,
    ) -> str:
        """Возвращает имя типа атрибута по его GUID.

        Мост «GUID → имя»: переводит стабильный GUID типа атрибута в человекочитаемое имя
        из метаданных (для логов, UI, отчётов). Ответ сервера — строка (имя), а не
        объект-обёртка.

        Когда применять: чтобы показать понятное имя по сохранённому стабильному GUID, не
        загружая полное метаописание (:meth:`attribute_type_by_guid`). Аналог по id —
        :meth:`attribute_type_name`; обратное направление — :meth:`attribute_type_guid_by_name`.

        Args:
            guid: GUID типа атрибута (стабильный идентификатор типа в id-пространстве
                ТИПОВ атрибутов), строка вида ``cad001c5-306c-11d8-b4e9-00304f19f545``.

        Returns:
            Имя типа атрибута как строка. Пустая строка, если сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если тип атрибута с таким
                GUID не найден).

        Example:
            async with IPSClient(config=config) as ips:
                name = await ips.attribute_type_name_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_GetAttributeTypeNameByGuid``; путь
            ``GET /core/api/metadata/attributeTypes/byGuid/{guid}/name``. Связанные методы:
            :meth:`attribute_type_name`, :meth:`attribute_type_guid_by_name`.
        """
        path = f"/core/api/metadata/attributeTypes/byGuid/{guid}/name"
        data = await self._request("get", path)
        return "" if data is None else str(data)
