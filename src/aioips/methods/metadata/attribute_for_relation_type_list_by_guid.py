"""Метод получения списка атрибутов типа связи по GUID."""

from uuid import UUID

from ...core import APIManager
from ...schemas.metadata import AttributeForRelationType


class AttributeForRelationTypeListByGuidMixin(APIManager):
    """Реализует ``GET attributeForRelationTypeList/byGuid/{relationTypeGuid}``."""

    async def attribute_for_relation_type_list_by_guid(
        self: "AttributeForRelationTypeListByGuidMixin",
        relation_type_guid: UUID | str,
    ) -> list[AttributeForRelationType]:
        """Возвращает список атрибутов, применимых к типу связи, по его GUID.

        Тот же результат, что у :meth:`attribute_for_relation_type_list`, но ключ —
        переносимый между базами GUID типа связи. Отдаёт «привязки» типов атрибутов к
        указанному типу связи вместе с переопределёнными для каждой пары параметрами
        (обязательность/видимость, формула, ограничения ссылок). Ответ — голый массив
        DTO без обёртки ``...NullableResultDto``.

        Когда применять: чтобы по GUID типа связи узнать весь набор его атрибутов и их
        настройки (например, в коде, работающем с несколькими инсталляциями IPS).

        Args:
            relation_type_guid: GUID типа связи (``UUID`` или строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Подставляется в URL как есть.

        Returns:
            Список настроек атрибутов по схеме :class:`AttributeForRelationType`. Пустой
            список — у типа связи нет привязанных атрибутов (или тип не найден: сервер
            для несуществующего GUID возвращает пустую коллекцию, а не ошибку).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                attrs = await ips.attribute_for_relation_type_list_by_guid(
                    "22222222-2222-2222-2222-222222222222"
                )
                print(len(attrs))

        Notes:
            operationId ``Metadata_GetAttributeForRelationTypeListByGuid``; путь
            ``GET /core/api/metadata/attributeForRelationTypeList/byGuid/{relationTypeGuid}``.
            Аналог по числовому id — :meth:`attribute_for_relation_type_list`.
        """
        path = f"/core/api/metadata/attributeForRelationTypeList/byGuid/{relation_type_guid}"
        data = await self._request("get", path)
        return [AttributeForRelationType.model_validate(item) for item in data]
