"""Метод получения значений атрибута объекта по GUID объекта."""

from typing import Any
from urllib.parse import quote
from uuid import UUID

from ...core import APIManager


class ObjectAttributeValuesByGuidMixin(APIManager):
    """Реализует ``GET /objects/{objectGuid}/attributes/{attributeId}/by-guid/values``.

    Соответствует операции ``ObjectAttributes_GetAttributeValuesByGuid``.
    """

    async def object_attribute_values_by_guid(
        self: "ObjectAttributeValuesByGuidMixin",
        object_guid: UUID | str,
        attribute_id: int,
    ) -> list[Any] | None:
        """Возвращает список «сырых» значений атрибута объекта, заданного по GUID.

        GUID-аналог :meth:`object_attribute_values`: когда известен GUID объекта, а не
        числовой ``objectID``. Возвращает сами значения характеристики без метаданных
        атрибута. Атрибут может быть множественным, поэтому всегда список; типы значений
        зависят от ``FieldTypes`` атрибута (строка/число/дата/ссылка), поэтому элементы —
        произвольные JSON-значения. Для атрибута-ссылки (``ftObjectLink``) элемент — id
        связанного объекта. Только чтение — checkout не требуется.

        Предусловие по id-пространству: ``object_guid`` — это ``objectGUID`` (GUID
        ОБЪЕКТА, общий для всех версий), а НЕ ``guid`` версии.

        Args:
            object_guid: GUID ОБЪЕКТА (``objectGUID``), общий для всех версий. Принимает
                ``uuid.UUID`` или строку канонического вида ``8-4-4-4-12``; кодируется в
                URL.
            attribute_id: Идентификатор ТИПА атрибута (какую характеристику читать).

        Returns:
            Список значений атрибута (возможно пустой) или ``None``, если значения не
            заданы/атрибут отсутствует (сервер вернул ``entity = null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                values = await ips.object_attribute_values_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545", 12
                )

        Notes:
            ``operationId``: ``ObjectAttributes_GetAttributeValuesByGuid``. Ответ —
            result-обёртка ``{entity, isEntityPresent}`` (``ObjectArrayNullableResultDto``,
            ``entity`` — массив), разворачивается в ``list | None``. См.
            :meth:`object_attribute_values`.
        """
        encoded_guid = quote(str(object_guid), safe="")
        path = f"/core/api/objects/{encoded_guid}/attributes/{attribute_id}/by-guid/values"
        data = await self._request("get", path)
        if not isinstance(data, dict):
            return None
        entity = data.get("entity")
        return list(entity) if entity is not None else None
