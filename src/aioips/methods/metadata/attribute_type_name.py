"""Метод получения имени типа атрибута по идентификатору."""

from ...core import APIManager


class AttributeTypeNameMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeTypes/{id}/name``."""

    async def attribute_type_name(
        self: "AttributeTypeNameMixin",
        attribute_type_id: int,
    ) -> str:
        """Возвращает имя типа атрибута по его идентификатору.

        Мост «id → имя»: переводит числовой ``id`` типа атрибута в человекочитаемое имя
        из метаданных (для логов, UI, отчётов). Ответ сервера — строка (имя), а не
        объект-обёртка.

        Когда применять: чтобы показать понятное имя по уже известному ``id`` (например,
        из :meth:`attribute_for_object_type_list` или :meth:`attribute_type_ids`), не загружая
        полное метаописание (:meth:`attribute_type`). Аналог по GUID —
        :meth:`attribute_type_name_by_guid`; обратное направление —
        :meth:`attribute_type_id_by_name`.

        Args:
            attribute_type_id: Идентификатор типа атрибута (id-пространство ТИПОВ
                атрибутов метаданных, не значение атрибута объекта).

        Returns:
            Имя типа атрибута как строка. Пустая строка, если сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если тип атрибута с таким
                ``id`` не найден).

        Example:
            async with IPSClient(config=config) as ips:
                name = await ips.attribute_type_name(1029)

        Notes:
            operationId ``Metadata_GetAttributeTypeNameById``; путь
            ``GET /core/api/metadata/attributeTypes/{id}/name``. Связанные методы:
            :meth:`attribute_type_name_by_guid`, :meth:`attribute_type_id_by_name`.
        """
        path = f"/core/api/metadata/attributeTypes/{attribute_type_id}/name"
        data = await self._request("get", path)
        return "" if data is None else str(data)
