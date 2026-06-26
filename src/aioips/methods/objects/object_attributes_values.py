"""Метод получения значений всех атрибутов объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import AttributeValues


class ObjectAttributesValuesMixin(APIManager):
    """Реализует ``ObjectAttributes_GetAttributesValues`` (значения всех атрибутов)."""

    async def object_attributes_values(
        self: "ObjectAttributesValuesMixin",
        object_id: int,
        *,
        extend_by_type: bool = False,
        attribute_values_modes: str | None = None,
    ) -> list[AttributeValues]:
        """Возвращает значения всех атрибутов объекта с расширенными метаданными.

        Самый подробный способ прочитать атрибуты: в отличие от :meth:`object_attributes`,
        для каждого атрибута дополнительно отдаёт GUID, псевдоним, режим множественности
        (``MultiValueModes``) и режим вычисления (``ComputeValueModes``), а также
        извлечённые (разрешённые) значения. Применяйте, когда нужны эти метаданные;
        иначе достаточно :meth:`object_attributes`. Только чтение — checkout не нужен.

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для
                всех версий. Не идентификатор версии (``id`` / F_ID).
            extend_by_type: Если ``True``, дополнить сведениями о типе атрибута
                (``attribute_type_info``). По умолчанию ``False``.
            attribute_values_modes: Флаги выборки значений (enum-строка
                ``GetAttributeValuesModes``: включать имя/GUID/псевдоним/blob'ы/описания,
                проверять доступ на запись/видимость и т.п.). ``None`` — серверный режим
                по умолчанию.

        Returns:
            Список значений атрибутов по схеме :class:`AttributeValues` (пустой список,
            если атрибутов нет). У каждого: ``attribute_id``, ``attribute_type``
            (``FieldTypes``), ``values``, ``multiple_valued``, ``compute_mode``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                values = await ips.object_attributes_values(102550)
                by_id = {v.attribute_id: v.values for v in values}

        Notes:
            ``operationId``: ``ObjectAttributes_GetAttributesValues``. IPS может отдавать
            ``null`` вместо ``[]`` для пустых списков (``descriptions`` и др.) — схема это
            нормализует. См. граблям и объектной модели IPS (раздел «Атрибуты»).
        """
        params: dict[str, Any] = {"isNeedToExtendByAttributeType": str(extend_by_type).lower()}
        if attribute_values_modes is not None:
            params["attributeValuesModes"] = attribute_values_modes
        data = await self._request(
            "get", f"/core/api/objects/{object_id}/attributesValues", params=params
        )
        items = data if isinstance(data, list) else []
        return [AttributeValues.model_validate(item) for item in items]
