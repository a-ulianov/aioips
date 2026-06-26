"""Метод получения всех привязок одного атрибута ко всем типам связей."""

from ...core import APIManager
from ...schemas.metadata import AttributeForRelationType


class AllAttributesForRelationTypeListMixin(APIManager):
    """Реализует ``GET allAttributesForRelationTypeList/{attributeTypeId}``."""

    async def all_attributes_for_relation_type_list(
        self: "AllAttributesForRelationTypeListMixin",
        attribute_type_id: int,
    ) -> list[AttributeForRelationType]:
        """Возвращает все привязки заданного атрибута ко всем типам связей.

        Обратный срез по сравнению с :meth:`attribute_for_relation_type_list`: тот метод
        фиксирует тип связи и перечисляет его атрибуты, а этот фиксирует тип атрибута и
        перечисляет ВСЕ типы связей, к которым он применён, вместе с их индивидуальными
        настройками (поле ``relation_type_id`` различает строки). Ответ — голый массив
        DTO без обёртки ``...NullableResultDto``.

        Когда применять: чтобы узнать, в каких типах связей используется конкретный
        атрибут и с какими настройками (например, при анализе влияния изменения
        метаданных атрибута). ``id`` атрибута — из :meth:`attribute_types`/
        :meth:`attribute_type_id_by_name`.

        Args:
            attribute_type_id: Идентификатор типа атрибута (id-пространство ТИПОВ
                атрибутов, не значение атрибута связи).

        Returns:
            Список настроек по схеме :class:`AttributeForRelationType` (по одной на
            каждый тип связи, где атрибут применён). Пустой список — атрибут не привязан
            ни к одному типу связи.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                bindings = await ips.all_attributes_for_relation_type_list(1029)
                relation_types = [b.relation_type_id for b in bindings]

        Notes:
            operationId ``Metadata_GetAllAttributesForRelationTypeListById``; путь
            ``GET /core/api/metadata/allAttributesForRelationTypeList/{attributeTypeId}``.
            Аналог по GUID — :meth:`all_attributes_for_relation_type_list_by_guid`.
        """
        path = f"/core/api/metadata/allAttributesForRelationTypeList/{attribute_type_id}"
        data = await self._request("get", path)
        return [AttributeForRelationType.model_validate(item) for item in data]
