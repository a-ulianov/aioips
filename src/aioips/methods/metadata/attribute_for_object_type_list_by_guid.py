"""Метод получения списка атрибутов типа объекта по GUID."""

from uuid import UUID

from ...core import APIManager
from ...schemas.metadata import AttributeForObjectType


class AttributeForObjectTypeListByGuidMixin(APIManager):
    """Реализует ``GET attributeForObjectTypeList/byGuid/{objectTypeGuid}``."""

    async def attribute_for_object_type_list_by_guid(
        self: "AttributeForObjectTypeListByGuidMixin",
        object_type_guid: UUID | str,
    ) -> list[AttributeForObjectType]:
        """Возвращает список атрибутов, применимых к типу объекта, по его GUID.

        Тот же результат, что у :meth:`attribute_for_object_type_list`, но ключ —
        переносимый между базами GUID типа объекта. Отдаёт «привязки» типов атрибутов к
        указанному типу объекта вместе с переопределёнными для каждой пары параметрами
        (обязательность/видимость, формула, ограничения ссылок). Ответ — голый массив
        DTO без обёртки ``...NullableResultDto``.

        Когда применять: чтобы по GUID типа объекта узнать весь набор его атрибутов и
        их настройки (например, в коде, работающем с несколькими инсталляциями IPS).

        Args:
            object_type_guid: GUID типа объекта (``UUID`` или строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Подставляется в URL как есть.

        Returns:
            Список настроек атрибутов по схеме :class:`AttributeForObjectType`. Пустой
            список — у типа нет привязанных атрибутов (или тип не найден: сервер для
            несуществующего GUID возвращает пустую коллекцию, а не ошибку).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                attrs = await ips.attribute_for_object_type_list_by_guid(
                    "11111111-1111-1111-1111-111111111111"
                )
                ids = [a.attribute_id for a in attrs]

        Notes:
            operationId ``Metadata_GetAttributeForObjectTypeListByGuid``; путь
            ``GET /core/api/metadata/attributeForObjectTypeList/byGuid/{objectTypeGuid}``.
            Связанный метод по числовому id — :meth:`attribute_for_object_type_list`.
        """
        path = f"/core/api/metadata/attributeForObjectTypeList/byGuid/{object_type_guid}"
        data = await self._request("get", path)
        return [AttributeForObjectType.model_validate(item) for item in data]
