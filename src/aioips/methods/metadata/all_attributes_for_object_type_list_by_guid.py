"""Метод получения всех привязок атрибута ко всем типам объектов по GUID."""

from uuid import UUID

from ...core import APIManager
from ...schemas.metadata import AttributeForObjectType


class AllAttributesForObjectTypeListByGuidMixin(APIManager):
    """Реализует ``GET allAttributesForObjectTypeList/byGuid/{attributeTypeGuid}``."""

    async def all_attributes_for_object_type_list_by_guid(
        self: "AllAttributesForObjectTypeListByGuidMixin",
        attribute_type_guid: UUID | str,
    ) -> list[AttributeForObjectType]:
        """Возвращает все привязки атрибута ко всем типам объектов по GUID атрибута.

        Тот же результат, что у :meth:`all_attributes_for_object_type_list`, но ключ —
        переносимый между базами GUID типа атрибута. Перечисляет все типы объектов, к
        которым применён данный атрибут, вместе с их индивидуальными настройками (поле
        ``object_type_id`` различает строки). Ответ — голый массив DTO без обёртки
        ``...NullableResultDto``.

        Когда применять: тот же анализ «где используется атрибут», но в коде, работающем
        с несколькими инсталляциями IPS (идентификация по GUID).

        Args:
            attribute_type_guid: GUID типа атрибута (``UUID`` или строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Подставляется в URL как есть.

        Returns:
            Список настроек по схеме :class:`AttributeForObjectType` (по одной на каждый
            тип объекта, где атрибут применён). Пустой список — атрибут не привязан ни к
            одному типу объекта.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                bindings = await ips.all_attributes_for_object_type_list_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(len(bindings))

        Notes:
            operationId ``Metadata_GetAllAttributesForObjectTypeListByGuid``; путь
            ``GET /core/api/metadata/allAttributesForObjectTypeList/byGuid/{attributeTypeGuid}``.
            Аналог по числовому id — :meth:`all_attributes_for_object_type_list`.
        """
        path = f"/core/api/metadata/allAttributesForObjectTypeList/byGuid/{attribute_type_guid}"
        data = await self._request("get", path)
        return [AttributeForObjectType.model_validate(item) for item in data]
