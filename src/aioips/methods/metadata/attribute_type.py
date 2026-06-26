"""Метод получения типа атрибута по идентификатору."""

from ...core import APIManager
from ...schemas.metadata import AttributeType


class AttributeTypeMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeTypes/{id}``."""

    async def attribute_type(
        self: "AttributeTypeMixin",
        attribute_type_id: int,
    ) -> AttributeType | None:
        """Возвращает описание типа атрибута по его идентификатору.

        Тип атрибута задаёт метаописание характеристики объекта: тип данных
        (``FieldTypes``), режим множественности и вычисляемости значений. Ответ сервера
        обёрнут в ``...NullableResultDto`` (``{entity, isEntityPresent}``); обёртка
        разворачивается здесь, наружу отдаётся либо схема, либо ``None``.

        Когда применять: чтобы по известному ``id`` атрибута получить его полное
        метаописание (например, узнать ``field_type`` перед чтением/записью значения, или
        ``possible_values`` для атрибута из списка). ``id`` берётся из
        :meth:`attribute_types`, :meth:`attribute_type_id_by_name` или из привязок
        :meth:`attribute_for_object_type_list`. Аналог по GUID — :meth:`attribute_type_by_guid`.

        Args:
            attribute_type_id: Идентификатор типа атрибута (id-пространство ТИПОВ
                атрибутов метаданных, не значение атрибута объекта).

        Returns:
            Тип атрибута по схеме :class:`AttributeType` либо ``None``, если тип атрибута
            с таким идентификатором не найден (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                attr = await ips.attribute_type(1029)
                if attr is not None:
                    print(attr.name, attr.field_type)

        Notes:
            operationId ``Metadata_GetAttributeType``; путь
            ``GET /core/api/metadata/attributeTypes/{id}``.
        """
        data = await self._request("get", f"/core/api/metadata/attributeTypes/{attribute_type_id}")
        entity = data.get("entity") if isinstance(data, dict) else None
        return AttributeType.model_validate(entity) if entity is not None else None
