"""Метод получения идентификатора группы атрибутов по GUID."""

from urllib.parse import quote

from ...core import APIManager


class AttributeGroupIdByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeGroups/byGuid/{guid}/id``."""

    async def attribute_group_id_by_guid(
        self: "AttributeGroupIdByGuidMixin",
        guid: str,
    ) -> int:
        """Возвращает идентификатор группы атрибутов по её GUID.

        Мост «GUID → id»: GUID группы атрибутов стабилен между установками IPS, а методы
        чтения принимают числовой ``id`` текущей среды. Метод переводит переносимый GUID
        в локальный ``id``. Ответ сервера — целое число (идентификатор), а не
        объект-обёртка.

        Когда применять: когда конфигурация хранит стабильный GUID группы, но для вызова
        нужен числовой ``id`` текущей среды. Обратное направление —
        :meth:`attribute_group_guid`.

        Args:
            guid: GUID группы атрибутов (стабильный идентификатор в id-пространстве
                ГРУПП атрибутов), строка вида ``cad001c5-306c-11d8-b4e9-00304f19f545``;
                кодируется в URL.

        Returns:
            Числовой идентификатор группы атрибутов (``id`` из id-пространства ГРУПП
            атрибутов). Сервер не возвращает ``None``: при отсутствии GUID — ошибка.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если группа с таким
                GUID не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                group_id = await ips.attribute_group_id_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_GetAttributeGroupId``; путь
            ``GET /core/api/metadata/attributeGroups/byGuid/{guid}/id``. Связанные методы:
            :meth:`attribute_group_guid`, :meth:`attribute_group_by_guid`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/attributeGroups/byGuid/{encoded_guid}/id"
        data = await self._request("get", path)
        return int(data)
