"""Метод получения настройки атрибута для типа связи по идентификаторам."""

from ...core import APIManager
from ...schemas.metadata import AttributeForRelationType


class AttributeForRelationTypeMixin(APIManager):
    """Реализует ``GET attributeForRelationType/{relationTypeId}/{attributeTypeId}``."""

    async def attribute_for_relation_type(
        self: "AttributeForRelationTypeMixin",
        relation_type_id: int,
        attribute_type_id: int,
    ) -> AttributeForRelationType | None:
        """Возвращает настройку применения одного атрибута к одному типу связи.

        Атрибуты могут навешиваться не только на объекты, но и на связи между ними
        (``RelationType``). Этот метод адресует конкретную пару «тип связи × тип
        атрибута» и отдаёт её индивидуальные настройки: обязательность/видимость
        (``required``), вычисляемость, формулу, ограничение ссылки. Ответ сервера
        обёрнут в ``...NullableResultDto`` (``{entity, isEntityPresent}``); обёртка
        разворачивается здесь, наружу отдаётся либо схема, либо ``None``.

        Когда применять: чтобы точечно узнать, применим ли данный атрибут к данному
        типу связи и с какими настройками. Весь список атрибутов связи —
        :meth:`attribute_for_relation_type_list`; аналог по GUID —
        :meth:`attribute_for_relation_type_by_guids`.

        Args:
            relation_type_id: Идентификатор типа связи (``RelationTypeID`` из
                :meth:`relation_types_meta`) — id-пространство ТИПОВ связей, не
                идентификатор конкретной связи (``RelationID``).
            attribute_type_id: Идентификатор типа атрибута (id-пространство ТИПОВ
                атрибутов, из :meth:`attribute_types`/:meth:`attribute_type_id_by_name`).

        Returns:
            Настройка по схеме :class:`AttributeForRelationType` либо ``None``, если
            атрибут к данному типу связи не привязан (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                binding = await ips.attribute_for_relation_type(500, 1029)
                if binding is not None:
                    print(binding.required, binding.field_type)

        Notes:
            operationId ``Metadata_GetAttributeForRelationTypeByIds``; путь
            ``GET /core/api/metadata/attributeForRelationType/{relationTypeId}/{attributeTypeId}``.
            Связанные методы: :meth:`attribute_for_relation_type_by_guids`,
            :meth:`attribute_for_relation_type_list`.
        """
        path = f"/core/api/metadata/attributeForRelationType/{relation_type_id}/{attribute_type_id}"
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return AttributeForRelationType.model_validate(entity) if entity is not None else None
