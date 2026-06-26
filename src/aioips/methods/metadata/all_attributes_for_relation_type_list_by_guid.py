"""Метод получения всех привязок атрибута ко всем типам связей по GUID."""

from uuid import UUID

from ...core import APIManager
from ...schemas.metadata import AttributeForRelationType


class AllAttributesForRelationTypeListByGuidMixin(APIManager):
    """Реализует ``GET allAttributesForRelationTypeList/byGuid/{attributeTypeGuid}``."""

    async def all_attributes_for_relation_type_list_by_guid(
        self: "AllAttributesForRelationTypeListByGuidMixin",
        attribute_type_guid: UUID | str,
    ) -> list[AttributeForRelationType]:
        """Возвращает все привязки атрибута ко всем типам связей по GUID атрибута.

        Тот же результат, что у :meth:`all_attributes_for_relation_type_list`, но ключ —
        переносимый между базами GUID типа атрибута. Перечисляет все типы связей, к
        которым применён данный атрибут, вместе с их индивидуальными настройками (поле
        ``relation_type_id`` различает строки). Ответ — голый массив DTO без обёртки
        ``...NullableResultDto``.

        Когда применять: тот же анализ «где используется атрибут», но в коде, работающем
        с несколькими инсталляциями IPS (идентификация по GUID).

        Args:
            attribute_type_guid: GUID типа атрибута (``UUID`` или строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Подставляется в URL как есть.

        Returns:
            Список настроек по схеме :class:`AttributeForRelationType` (по одной на
            каждый тип связи, где атрибут применён). Пустой список — атрибут не привязан
            ни к одному типу связи.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                bindings = await ips.all_attributes_for_relation_type_list_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(len(bindings))

        Notes:
            operationId ``Metadata_GetAllAttributesForRelationTypeListByGuid``; путь
            ``GET /core/api/metadata/allAttributesForRelationTypeList/byGuid/{attributeTypeGuid}``.
            Аналог по числовому id — :meth:`all_attributes_for_relation_type_list`.
        """
        path = f"/core/api/metadata/allAttributesForRelationTypeList/byGuid/{attribute_type_guid}"
        data = await self._request("get", path)
        return [AttributeForRelationType.model_validate(item) for item in data]
