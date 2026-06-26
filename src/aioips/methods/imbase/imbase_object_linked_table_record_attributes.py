"""Метод получения атрибутов записи таблицы справочника, связанной с объектом."""

from ...core import APIManager
from ...schemas.objects import AttributeValues


class ImBaseObjectLinkedTableRecordAttributesMixin(APIManager):
    """Реализует ``GET .../object/{objectId}/linkedImBaseTableRecord/attributes``.

    operationId ``ImBase_GetObjectLinkedImBaseTableRecordAttributes``.
    """

    async def imbase_object_linked_table_record_attributes(
        self: "ImBaseObjectLinkedTableRecordAttributesMixin",
        object_id: int,
    ) -> list[AttributeValues] | None:
        """Возвращает атрибуты записи таблицы справочника IMBASE, связанной с объектом.

        Объект предметной области может быть связан с конкретной записью табличной части
        справочника IMBASE; метод отдаёт значения атрибутов этой связанной записи вместе с
        метаданными типа (имя, GUID, псевдоним, ``FieldType``). Ответ обёрнут в
        ``...IEnumerableNullableResultDto`` (``{entity, isEntityPresent}``); обёртка
        разворачивается здесь, наружу отдаётся либо список значений, либо ``None``.

        Когда применять: чтобы по объекту получить «справочные» атрибуты из связанной с ним
        записи таблицы IMBASE. Аналогичная форма значений возвращается
        :meth:`classificator_attributes`. Предусловий нет (операция чтения).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectId`` / F_OBJECT_ID — общий для всех
                версий, как у :meth:`object_get`), НЕ id версии (F_ID).

        Returns:
            Список значений атрибутов по схеме :class:`AttributeValues` (``attribute_id``,
            ``attribute_name``, ``attribute_guid``, ``attribute_alias``, ``attribute_type``
            и список ``values``), либо ``None``, если entity отсутствует
            (``isEntityPresent == false`` — у объекта нет связанной записи). Пустой список —
            запись связана, но атрибутов не отдано.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                attrs = await ips.imbase_object_linked_table_record_attributes(102550)
                if attrs is not None:
                    for a in attrs:
                        print(a.attribute_name, a.values)

        Notes:
            operationId ``ImBase_GetObjectLinkedImBaseTableRecordAttributes``; путь
            ``GET /core/api/imbase/object/{objectId}/linkedImBaseTableRecord/attributes``
            (``...IEnumerableNullableResultDto`` → entity-массив). Схема
            :class:`AttributeValues` переиспользуется из раздела объектов. См.
            [[ips-object-model]] (разделы «Идентичность», «Атрибуты»).
        """
        data = await self._request(
            "get",
            f"/core/api/imbase/object/{object_id}/linkedImBaseTableRecord/attributes",
        )
        entity = data.get("entity") if isinstance(data, dict) else None
        if entity is None:
            return None
        return [AttributeValues.model_validate(item) for item in entity]
