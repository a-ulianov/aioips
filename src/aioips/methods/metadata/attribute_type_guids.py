"""Метод получения списка GUID всех типов атрибутов."""

from ...core import APIManager


class AttributeTypeGuidsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeTypes/guids``."""

    async def attribute_type_guids(
        self: "AttributeTypeGuidsMixin",
    ) -> list[str]:
        """Возвращает список GUID всех типов атрибутов метаданных.

        Плоский перечень стабильных GUID всех зарегистрированных типов атрибутов. GUID
        переносимы между установками IPS (в отличие от ``id``), поэтому подходят для сверки
        конфигурации между средами. Ответ сервера — массив строк, без обёртки
        ``...NullableResultDto``.

        Когда применять: для инвентаризации/сравнения наборов типов атрибутов между
        средами по стабильным GUID. Перечень числовых id — :meth:`attribute_type_ids`;
        перевод GUID → id — :meth:`attribute_type_id_by_guid`.

        Returns:
            Список GUID типов атрибутов (строки в id-пространстве ТИПОВ атрибутов).
            Пустой список — типов атрибутов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.attribute_type_guids()
                print(len(guids))

        Notes:
            operationId ``Metadata_GetAttributeTypeGuidList``; путь
            ``GET /core/api/metadata/attributeTypes/guids`` (ответ — массив строк).
            Связанные методы: :meth:`attribute_type_ids`, :meth:`attribute_type_id_by_guid`.
        """
        path = "/core/api/metadata/attributeTypes/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
