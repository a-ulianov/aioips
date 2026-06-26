"""Метод получения одного атрибута объекта по идентификатору типа атрибута."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import Attribute


class ObjectAttributeMixin(APIManager):
    """Реализует ``ObjectAttributes_GetAttribute`` (атрибут объекта по id типа)."""

    async def object_attribute(
        self: "ObjectAttributeMixin",
        object_id: int,
        attribute_id: int,
        *,
        get_actual_copy: bool = False,
        extend_by_type: bool = False,
        throw_not_found: bool = False,
    ) -> Attribute | None:
        """Возвращает один атрибут объекта по идентификатору типа атрибута.

        Точечное чтение одной характеристики, когда известен id типа атрибута (дешевле,
        чем тянуть все атрибуты через :meth:`object_attributes`). Только чтение —
        checkout не нужен. Для одних лишь значений (без метаданных атрибута) есть
        :meth:`object_attribute_values`.

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для
                всех версий. Не идентификатор версии (``id`` / F_ID).
            attribute_id: Идентификатор ТИПА атрибута (какую характеристику читать).
            get_actual_copy: Если ``True``, вернуть значение из актуальной копии объекта.
                По умолчанию ``False``.
            extend_by_type: Если ``True``, дополнить сведениями о типе атрибута
                (``attribute_type_info``). По умолчанию ``False``.
            throw_not_found: Если ``True``, при отсутствии атрибута сервер вернёт ошибку
                (метод поднимет исключение); иначе метод вернёт ``None``.

        Returns:
            Атрибут по схеме :class:`Attribute` или ``None``, если он не найден
            (и ``throw_not_found`` равно ``False``).

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404 при ``throw_not_found``).

        Example:
            async with IPSClient(config=config) as ips:
                attr = await ips.object_attribute(102550, 12)
                if attr is not None:
                    print(attr.as_string)

        Notes:
            ``operationId``: ``ObjectAttributes_GetAttribute``. Ответ — result-обёртка
            ``{entity, isEntityPresent}``, разворачивается в ``Attribute | None``.
        """
        params: dict[str, Any] = {
            "getActualCopy": str(get_actual_copy).lower(),
            "isNeedToExtendByAttributeType": str(extend_by_type).lower(),
            "throwNotFoundException": str(throw_not_found).lower(),
        }
        data = await self._request(
            "get",
            f"/core/api/objects/{object_id}/attributes/{attribute_id}",
            params=params,
        )
        entity = data.get("entity") if isinstance(data, dict) else None
        return Attribute.model_validate(entity) if entity is not None else None
