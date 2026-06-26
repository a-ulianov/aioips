"""Метод получения настройки атрибута для типа объекта по идентификаторам."""

from ...core import APIManager
from ...schemas.metadata import AttributeForObjectType


class AttributeForObjectTypeMixin(APIManager):
    """Реализует ``GET attributeForObjectType/{objectTypeId}/{attributeTypeId}``."""

    async def attribute_for_object_type(
        self: "AttributeForObjectTypeMixin",
        object_type_id: int,
        attribute_type_id: int,
    ) -> AttributeForObjectType | None:
        """Возвращает настройку применения одного атрибута к одному типу объекта.

        В отличие от :meth:`attribute_for_object_type_list` (весь список привязок типа),
        этот метод адресует конкретную пару «тип объекта × тип атрибута» и отдаёт
        её индивидуальные настройки: обязательность/видимость (``required``),
        вычисляемость, формулу, ограничение ссылки и т.д. Ответ сервера обёрнут в
        ``...NullableResultDto`` (``{entity, isEntityPresent}``); обёртка
        разворачивается здесь, наружу отдаётся либо схема, либо ``None``.

        Когда применять: чтобы точечно узнать, применим ли данный атрибут к данному
        типу объекта и с какими настройками (например, перед чтением/записью значения).
        Аналог по GUID — :meth:`attribute_for_object_type_by_guids`.

        Args:
            object_type_id: Идентификатор типа объекта (``ObjectTypeID`` из
                :meth:`object_types`) — id-пространство ТИПОВ объектов, не ``ObjectID``
                конкретного объекта.
            attribute_type_id: Идентификатор типа атрибута (id-пространство ТИПОВ
                атрибутов, из :meth:`attribute_types`/:meth:`attribute_type_id_by_name`).

        Returns:
            Настройка по схеме :class:`AttributeForObjectType` либо ``None``, если
            атрибут к данному типу объекта не привязан (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                binding = await ips.attribute_for_object_type(1742, 1029)
                if binding is not None:
                    print(binding.required, binding.field_type)

        Notes:
            operationId ``Metadata_GetAttributeForObjectTypeByIds``; путь
            ``GET /core/api/metadata/attributeForObjectType/{objectTypeId}/{attributeTypeId}``.
            Связанные методы: :meth:`attribute_for_object_type_by_guids`,
            :meth:`attribute_for_object_type_list`.
        """
        path = f"/core/api/metadata/attributeForObjectType/{object_type_id}/{attribute_type_id}"
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return AttributeForObjectType.model_validate(entity) if entity is not None else None
