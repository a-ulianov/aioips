"""Метод получения идентификатора типа атрибута по GUID."""

from ...core import APIManager


class AttributeTypeIdByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeTypes/byGuid/{guid}/id``."""

    async def attribute_type_id_by_guid(
        self: "AttributeTypeIdByGuidMixin",
        guid: str,
    ) -> int:
        """Возвращает идентификатор типа атрибута по его GUID.

        Мост «GUID → id»: GUID типа атрибута стабилен между установками IPS, а большинство
        методов чтения значений/условий поиска принимают числовой ``id``. Метод переводит
        переносимый GUID в локальный ``id``. Ответ сервера — целое число (идентификатор),
        а не объект-обёртка.

        Когда применять: когда конфигурация хранит стабильный GUID типа атрибута, но для
        вызова нужен числовой ``id`` текущей среды. Аналог «имя → id» —
        :meth:`attribute_type_id_by_name`; обратное направление — :meth:`attribute_type_guid`.

        Args:
            guid: GUID типа атрибута (стабильный идентификатор типа в id-пространстве
                ТИПОВ атрибутов), строка вида ``cad001c5-306c-11d8-b4e9-00304f19f545``.

        Returns:
            Числовой идентификатор типа атрибута (``id`` из id-пространства ТИПОВ
            атрибутов). Сервер не возвращает ``None``: при отсутствии GUID — ошибка.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если тип атрибута с таким
                GUID не найден).

        Example:
            async with IPSClient(config=config) as ips:
                attr_id = await ips.attribute_type_id_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_GetAttributeTypeId``; путь
            ``GET /core/api/metadata/attributeTypes/byGuid/{guid}/id``. Связанные методы:
            :meth:`attribute_type_guid`, :meth:`attribute_type_id_by_name`.
        """
        path = f"/core/api/metadata/attributeTypes/byGuid/{guid}/id"
        data = await self._request("get", path)
        return int(data)
