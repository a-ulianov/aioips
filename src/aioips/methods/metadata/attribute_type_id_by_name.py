"""Метод получения идентификатора типа атрибута по его имени."""

from urllib.parse import quote

from ...core import APIManager


class AttributeTypeIdByNameMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeTypes/byName/{attributeName}/id``."""

    async def attribute_type_id_by_name(
        self: "AttributeTypeIdByNameMixin",
        attribute_name: str,
    ) -> int:
        """Возвращает идентификатор типа атрибута по его имени.

        Удобно, когда известно человекочитаемое имя атрибута, но нужен числовой
        идентификатор для последующих запросов (например, для условий поиска или
        чтения значений атрибутов). Имя кодируется в URL, поэтому допускаются пробелы
        и кириллица. Ответ сервера — целое число (идентификатор), а не объект-обёртка.

        Когда применять: как мост «имя → id» перед вызовами, требующими ``attributeId``
        (условия поиска, чтение значений). Например, имя «Архив» → id ``1029`` для поиска
        документов архива. Полное метаописание по полученному id — :meth:`attribute_type`.

        Args:
            attribute_name: Имя типа атрибута точно как в метаданных IPS (регистр и
                пробелы значимы); кодируется в URL, кириллица допускается.

        Returns:
            Числовой идентификатор типа атрибута (``id`` из id-пространства типов
            атрибутов). Сервер не возвращает ``None``: при отсутствии имени — ошибка.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если атрибут с таким
                именем не найден).

        Example:
            async with IPSClient(config=config) as ips:
                attr_id = await ips.attribute_type_id_by_name("Архив")
                print(attr_id)

        Notes:
            operationId ``Metadata_GetAttributeTypeIdByName``; путь
            ``GET /core/api/metadata/attributeTypes/byName/{attributeName}/id``.
        """
        encoded_name = quote(attribute_name, safe="")
        path = f"/core/api/metadata/attributeTypes/byName/{encoded_name}/id"
        data = await self._request("get", path)
        return int(data)
