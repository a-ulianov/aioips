"""Метод получения GUID группы атрибутов по идентификатору."""

from ...core import APIManager


class AttributeGroupGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeGroups/{id}/guid``."""

    async def attribute_group_guid(
        self: "AttributeGroupGuidMixin",
        attribute_group_id: int,
    ) -> str:
        """Возвращает GUID группы атрибутов по её идентификатору.

        Мост «id → GUID»: переводит локальный числовой ``id`` группы атрибутов в
        стабильный GUID, переносимый между установками IPS. Ответ сервера — строка
        (GUID), а не объект-обёртка.

        Когда применять: чтобы сохранить переносимую ссылку на группу атрибутов (для
        сверки конфигурации между средами) по известному ``id`` текущей среды. Обратное
        направление — :meth:`attribute_group_id_by_guid`.

        Args:
            attribute_group_id: Идентификатор группы атрибутов (id-пространство ГРУПП
                атрибутов; не тип атрибута и не значение атрибута объекта).

        Returns:
            GUID группы атрибутов как строка. Пустая строка, если сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если группа с таким
                ``id`` не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                guid = await ips.attribute_group_guid(42)

        Notes:
            operationId ``Metadata_GetAttributeGroupGuid``; путь
            ``GET /core/api/metadata/attributeGroups/{id}/guid``. Связанные методы:
            :meth:`attribute_group_id_by_guid`, :meth:`attribute_group`.
        """
        path = f"/core/api/metadata/attributeGroups/{attribute_group_id}/guid"
        data = await self._request("get", path)
        return "" if data is None else str(data)
