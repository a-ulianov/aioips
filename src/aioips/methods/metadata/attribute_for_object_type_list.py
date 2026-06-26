"""Метод получения списка атрибутов, применимых к типу объекта."""

from ...core import APIManager
from ...schemas.metadata import AttributeForObjectType


class AttributeForObjectTypeListMixin(APIManager):
    """Реализует ``GET /core/api/metadata/attributeForObjectTypeList/{objectTypeId}``."""

    async def attribute_for_object_type_list(
        self: "AttributeForObjectTypeListMixin",
        object_type_id: int,
    ) -> list[AttributeForObjectType]:
        """Возвращает список типов атрибутов, применимых к заданному типу объекта.

        Один и тот же тип атрибута может применяться к разным типам объектов с
        индивидуальными настройками (обязательность, видимость, формула, ограничения).
        Метод отдаёт «привязки» типов атрибутов к указанному типу объекта вместе с
        переопределёнными для этой пары параметрами — это набор характеристик, которые
        объект данного типа может нести.

        Когда применять: чтобы узнать, какие атрибуты есть у объектов конкретного типа
        и с какими настройками (обязательность, формула, ссылочные ограничения) — например
        перед чтением/записью значений атрибутов или построением условий поиска. ``id`` типа
        объекта берётся из :meth:`object_types`; полное метаописание каждого атрибута (тип
        данных, множественность) — из :meth:`attribute_type`/:meth:`attribute_types`.

        Args:
            object_type_id: Идентификатор типа объекта (``ObjectTypeID`` из
                :meth:`object_types`) — id-пространство ТИПОВ объектов, не ``ObjectID``
                конкретного объекта.

        Returns:
            Список настроек атрибутов по схеме :class:`AttributeForObjectType`. Пустой
            список означает, что у типа нет привязанных атрибутов (или тип не найден —
            сервер для несуществующего типа возвращает пустую коллекцию, а не ошибку).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                attrs = await ips.attribute_for_object_type_list(1742)
                required = [a.attribute_id for a in attrs if a.required == "auto"]

        Notes:
            operationId ``Metadata_GetAttributeForObjectTypeList``; путь
            ``GET /core/api/metadata/attributeForObjectTypeList/{objectTypeId}``.
        """
        path = f"/core/api/metadata/attributeForObjectTypeList/{object_type_id}"
        data = await self._request("get", path)
        return [AttributeForObjectType.model_validate(item) for item in data]
