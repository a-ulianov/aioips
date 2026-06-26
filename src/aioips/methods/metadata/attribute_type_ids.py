"""Метод получения списка идентификаторов всех типов атрибутов."""

from ...core import APIManager


class AttributeTypeIdsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeTypes/ids``."""

    async def attribute_type_ids(
        self: "AttributeTypeIdsMixin",
    ) -> list[int]:
        """Возвращает список идентификаторов всех типов атрибутов метаданных.

        Плоский перечень числовых ``id`` всех зарегистрированных типов атрибутов. Ответ
        сервера — массив целых чисел, без обёртки ``...NullableResultDto``. Легче, чем
        :meth:`attribute_types` (полные схемы), когда нужны только идентификаторы.

        Когда применять: для обхода/инвентаризации типов атрибутов, когда достаточно
        идентификаторов (например, чтобы затем точечно дёрнуть :meth:`attribute_type` или
        :meth:`attribute_type_name` по нужным ``id``). Перечень GUID — :meth:`attribute_type_guids`.

        Returns:
            Список идентификаторов типов атрибутов (``id`` из id-пространства ТИПОВ
            атрибутов). Пустой список — типов атрибутов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.attribute_type_ids()
                print(len(ids))

        Notes:
            operationId ``Metadata_GetAttributeTypeIdList``; путь
            ``GET /core/api/metadata/attributeTypes/ids`` (ответ — массив ``int``).
            Связанные методы: :meth:`attribute_type_guids`, :meth:`attribute_types`.
        """
        path = "/core/api/metadata/attributeTypes/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
