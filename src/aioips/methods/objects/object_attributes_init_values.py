"""Метод получения начальных (инициализирующих) значений атрибутов объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import AttributeValues


class ObjectAttributesInitValuesMixin(APIManager):
    """Реализует ``ObjectAttributes_GetAttributesInitValues`` (начальные значения атрибутов)."""

    async def object_attributes_init_values(
        self: "ObjectAttributesInitValuesMixin",
        object_id: int,
        *,
        attr_ids: list[int] | None = None,
        extend_by_type: bool = False,
    ) -> list[AttributeValues]:
        """Возвращает начальные (инициализирующие) значения атрибутов объекта.

        Начальные значения — это значения по умолчанию, которыми атрибуты
        инициализируются по правилам типа/жизненного цикла (например, при создании или
        переходе на шаг ЖЦ), в отличие от текущих фактических значений из
        :meth:`object_attributes_values`. Применяйте, когда нужно понять, какими
        значениями атрибуты заполняются «из коробки». Структура ответа совпадает с
        :meth:`object_attributes_values` (схема :class:`AttributeValues`). Только
        чтение — checkout не нужен.

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для
                всех версий. Не идентификатор версии (``id`` / F_ID).
            attr_ids: Список идентификаторов ТИПОВ атрибутов, для которых нужны начальные
                значения. ``None`` (по умолчанию) — по всем атрибутам.
            extend_by_type: Если ``True``, дополнить каждый элемент сведениями о типе
                атрибута (``attribute_type_info``). По умолчанию ``False``.

        Returns:
            Список начальных значений атрибутов по схеме :class:`AttributeValues` (пустой
            список, если нет данных). У каждого: ``attribute_id``, ``attribute_type``
            (``FieldTypes``), ``values``, ``multiple_valued``, ``compute_mode``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                init = await ips.object_attributes_init_values(102550, attr_ids=[12])
                defaults = {v.attribute_id: v.values for v in init}

        Notes:
            ``operationId``: ``ObjectAttributes_GetAttributesInitValues``. Ответ — голый
            JSON-массив ``AttributeValuesDto`` (не result-обёртка). IPS может отдавать
            ``null`` вместо ``[]`` для пустых списков — схема это нормализует. См.
            [[gotchas]] и [[ips-object-model]] (раздел «Атрибуты»).
        """
        params: dict[str, Any] = {"isNeedToExtendByAttributeType": str(extend_by_type).lower()}
        if attr_ids is not None:
            params["attrIds"] = attr_ids
        data = await self._request(
            "get", f"/core/api/objects/{object_id}/attributesInitValues", params=params
        )
        items = data if isinstance(data, list) else []
        return [AttributeValues.model_validate(item) for item in items]
