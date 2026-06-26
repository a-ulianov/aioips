"""Метод получения значений атрибута объекта, ограниченных классификатором выбора."""

from ...core import APIManager
from ...schemas.objects import AttributeValues


class ClassificatorAttributesMixin(APIManager):
    """Реализует эндпоинт значений атрибута по классификатору выбора.

    ``GET /core/api/selectionClassificators/{classificatorId}/objects/{objectId}/attributeValues``;
    operationId ``SelectionClassificators_GetClasificatorAttributes``.
    """

    async def classificator_attributes(
        self: "ClassificatorAttributesMixin",
        classificator_id: int,
        object_id: int,
    ) -> list[AttributeValues]:
        """Возвращает значения атрибута объекта, ограниченные классификатором выбора.

        Классификатор выбора задаёт допустимый (классифицированный) набор значений для
        атрибута объекта. Метод применяет конкретный классификатор к конкретному объекту и
        отдаёт значения соответствующего атрибута вместе с метаданными типа (имя, GUID,
        псевдоним, тип данных ``FieldType``) и самими значениями.

        Когда применять: после того как через :meth:`classifiers_for_object_type` определён
        список классификаторов для типа объекта — чтобы для конкретного объекта получить
        значения атрибута, разрешённые/заданные данным классификатором.

        Предусловие по id-пространству (критично): ``object_id`` — это идентификатор
        ОБЪЕКТА (F_OBJECT_ID), общий для всех версий, как у :meth:`object_get`, а НЕ id
        версии (F_ID). ``classificator_id`` — id классификатора из
        :meth:`classifiers_for_object_type`.

        Args:
            classificator_id: Идентификатор классификатора выбора (из
                :meth:`classifiers_for_object_type`).
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для всех
                версий. Не id версии (F_ID).

        Returns:
            Список значений атрибутов по схеме :class:`AttributeValues`: для каждого —
            ``attribute_id``, ``attribute_name``, ``attribute_guid``, ``attribute_alias``,
            ``attribute_type`` (``FieldType``) и список ``values`` (для ``ftObjectLink`` —
            id объектов-целей). Голый массив без result-обёртки; пустой список означает,
            что классификатор не задаёт значений для этого объекта.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. если объект или классификатор
                не найдены).

        Example:
            async with IPSClient(config=config) as ips:
                attrs = await ips.classificator_attributes(204, 102550)  # 102550 = objectID
                for a in attrs:
                    print(a.attribute_name, a.values)

        Notes:
            operationId ``SelectionClassificators_GetClasificatorAttributes``; путь
            ``GET /core/api/selectionClassificators/{classificatorId}/objects/{objectId}/``
            ``attributeValues``. Схема :class:`AttributeValues` переиспользуется из раздела
            объектов. См. объектной модели IPS (разделы «Идентичность», «Атрибуты»).
        """
        data = await self._request(
            "get",
            f"/core/api/selectionClassificators/{classificator_id}"
            f"/objects/{object_id}/attributeValues",
        )
        return [AttributeValues.model_validate(item) for item in data]
