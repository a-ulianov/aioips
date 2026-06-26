"""Метод получения всех привязок одного атрибута ко всем типам объектов."""

from ...core import APIManager
from ...schemas.metadata import AttributeForObjectType


class AllAttributesForObjectTypeListMixin(APIManager):
    """Реализует ``GET allAttributesForObjectTypeList/{attributeTypeId}``."""

    async def all_attributes_for_object_type_list(
        self: "AllAttributesForObjectTypeListMixin",
        attribute_type_id: int,
    ) -> list[AttributeForObjectType]:
        """Возвращает все привязки заданного атрибута ко всем типам объектов.

        Обратный срез по сравнению с :meth:`attribute_for_object_type_list`: тот метод
        фиксирует тип объекта и перечисляет его атрибуты, а этот фиксирует тип атрибута
        и перечисляет ВСЕ типы объектов, к которым он применён, вместе с их
        индивидуальными настройками (поле ``object_type_id`` различает строки). Ответ —
        голый массив DTO без обёртки ``...NullableResultDto``.

        Когда применять: чтобы узнать, в каких типах объектов используется конкретный
        атрибут и с какими настройками (например, при анализе влияния изменения
        метаданных атрибута). ``id`` атрибута — из :meth:`attribute_types`/
        :meth:`attribute_type_id_by_name`.

        Args:
            attribute_type_id: Идентификатор типа атрибута (id-пространство ТИПОВ
                атрибутов, не значение атрибута объекта).

        Returns:
            Список настроек по схеме :class:`AttributeForObjectType` (по одной на каждый
            тип объекта, где атрибут применён). Пустой список — атрибут не привязан ни к
            одному типу объекта.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                bindings = await ips.all_attributes_for_object_type_list(1029)
                object_types = [b.object_type_id for b in bindings]

        Notes:
            operationId ``Metadata_GetAllAttributesForObjectTypeListById``; путь
            ``GET /core/api/metadata/allAttributesForObjectTypeList/{attributeTypeId}``.
            Аналог по GUID — :meth:`all_attributes_for_object_type_list_by_guid`.
        """
        path = f"/core/api/metadata/allAttributesForObjectTypeList/{attribute_type_id}"
        data = await self._request("get", path)
        return [AttributeForObjectType.model_validate(item) for item in data]
