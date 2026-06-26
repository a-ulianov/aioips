"""Метод получения GUID типа атрибута по его имени."""

from urllib.parse import quote

from ...core import APIManager


class AttributeTypeGuidByNameMixin(APIManager):
    """Реализует ``GET /core/api/metadata/attributeTypes/byName/{attributeName}/guid``."""

    async def attribute_type_guid_by_name(
        self: "AttributeTypeGuidByNameMixin",
        attribute_name: str,
    ) -> str:
        """Возвращает GUID типа атрибута по его имени.

        Мост «имя → GUID»: переводит человекочитаемое имя типа атрибута в стабильный GUID,
        переносимый между установками IPS. Имя кодируется в URL, поэтому допускаются
        пробелы и кириллица. Ответ сервера — строка (GUID), а не объект-обёртка.

        Когда применять: чтобы по известному имени получить переносимую ссылку на тип
        атрибута (для сверки конфигурации между средами), минуя локальный ``id``. Аналог
        «имя → id» — :meth:`attribute_type_id_by_name`; обратное направление —
        :meth:`attribute_type_name_by_guid`.

        Args:
            attribute_name: Имя типа атрибута точно как в метаданных IPS (регистр и
                пробелы значимы); кодируется в URL, кириллица допускается.

        Returns:
            GUID типа атрибута как строка. Пустая строка, если сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если атрибут с таким
                именем не найден).

        Example:
            async with IPSClient(config=config) as ips:
                guid = await ips.attribute_type_guid_by_name("Архив")

        Notes:
            operationId ``Metadata_GetAttributeTypeGuidByName``; путь
            ``GET /core/api/metadata/attributeTypes/byName/{attributeName}/guid``.
            Связанные методы: :meth:`attribute_type_id_by_name`,
            :meth:`attribute_type_name_by_guid`.
        """
        encoded_name = quote(attribute_name, safe="")
        path = f"/core/api/metadata/attributeTypes/byName/{encoded_name}/guid"
        data = await self._request("get", path)
        return "" if data is None else str(data)
