"""Метод получения списка атрибутов, применимых к типу связи."""

from ...core import APIManager
from ...schemas.metadata import AttributeForRelationType


class AttributeForRelationTypeListMixin(APIManager):
    """Реализует ``GET attributeForRelationTypeList/{relationTypeId}``."""

    async def attribute_for_relation_type_list(
        self: "AttributeForRelationTypeListMixin",
        relation_type_id: int,
    ) -> list[AttributeForRelationType]:
        """Возвращает список типов атрибутов, применимых к заданному типу связи.

        Аналог :meth:`attribute_for_object_type_list`, но для связей: перечисляет
        «привязки» типов атрибутов к указанному типу связи вместе с переопределёнными
        для каждой пары параметрами (обязательность/видимость, формула, ограничения
        ссылок) — это набор характеристик, которые связь данного типа может нести.
        Ответ — голый массив DTO без обёртки ``...NullableResultDto``.

        Когда применять: чтобы узнать, какие атрибуты есть у связей конкретного типа и
        с какими настройками (например, перед чтением/записью атрибутов связи). ``id``
        типа связи — из :meth:`relation_types_meta`; полное метаописание каждого
        атрибута — из :meth:`attribute_type`/:meth:`attribute_types`.

        Args:
            relation_type_id: Идентификатор типа связи (``RelationTypeID`` из
                :meth:`relation_types_meta`) — id-пространство ТИПОВ связей, не
                идентификатор конкретной связи (``RelationID``).

        Returns:
            Список настроек атрибутов по схеме :class:`AttributeForRelationType`. Пустой
            список — у типа связи нет привязанных атрибутов (или тип не найден: сервер
            для несуществующего типа возвращает пустую коллекцию, а не ошибку).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                attrs = await ips.attribute_for_relation_type_list(500)
                ids = [a.attribute_id for a in attrs]

        Notes:
            operationId ``Metadata_GetAttributeForRelationTypeListById``; путь
            ``GET /core/api/metadata/attributeForRelationTypeList/{relationTypeId}``.
            Аналог по GUID — :meth:`attribute_for_relation_type_list_by_guid`.
        """
        path = f"/core/api/metadata/attributeForRelationTypeList/{relation_type_id}"
        data = await self._request("get", path)
        return [AttributeForRelationType.model_validate(item) for item in data]
