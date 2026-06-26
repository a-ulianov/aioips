"""Метод получения всех атрибутов объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import Attribute


class ObjectAttributesMixin(APIManager):
    """Реализует ``ObjectAttributes_GetAttributes`` (все атрибуты объекта)."""

    async def object_attributes(
        self: "ObjectAttributesMixin",
        object_id: int,
        *,
        extend_by_type: bool = False,
    ) -> list[Attribute]:
        """Возвращает все атрибуты объекта вместе с их значениями.

        Чтение всех характеристик объекта (обозначение, наименование, масса, ссылки и
        т.п.) одним запросом. Это запрос только на чтение — режим редактирования
        (checkout) не требуется. Для получения одного атрибута используйте
        :meth:`object_attribute`; для расширенных метаданных (GUID, псевдоним, режимы
        множественности/вычисления) — :meth:`object_attributes_values`.

        Предусловие по id-пространству: аргумент — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для
                всех версий. Не идентификатор версии (``id`` / F_ID).
            extend_by_type: Если ``True``, дополнить каждый атрибут сведениями о типе
                (поле ``attribute_type_info``). По умолчанию ``False``.

        Returns:
            Список атрибутов по схеме :class:`Attribute` (пустой список, если их нет).
            У каждого: ``attribute_id`` (тип атрибута), ``name``, ``as_string``,
            ``values`` (типы зависят от ``data_type`` — см. ``FieldTypes``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                attributes = await ips.object_attributes(102550)
                values = {a.name: a.as_string for a in attributes}

        Notes:
            ``operationId``: ``ObjectAttributes_GetAttributes``. Видимость и права
            доступа влияют на состав возвращаемых атрибутов. См. [[ips-object-model]]
            (раздел «Атрибуты»).
        """
        params: dict[str, Any] = {"isNeedToExtendByAttributeType": str(extend_by_type).lower()}
        data = await self._request(
            "get", f"/core/api/objects/{object_id}/attributes", params=params
        )
        items = data if isinstance(data, list) else []
        return [Attribute.model_validate(item) for item in items]
