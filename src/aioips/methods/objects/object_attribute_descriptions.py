"""Метод получения описаний одного атрибута объекта."""

from typing import Any

from ...core import APIManager


class ObjectAttributeDescriptionsMixin(APIManager):
    """Реализует ``ObjectAttributes_GetAttributeDescriptions`` (описания одного атрибута)."""

    async def object_attribute_descriptions(
        self: "ObjectAttributeDescriptionsMixin",
        object_id: int,
        attribute_id: int,
        *,
        throw_not_found: bool = False,
    ) -> list[str] | None:
        """Возвращает текстовые описания значений одного атрибута объекта.

        Описание — это пояснительный текст к значению атрибута (например, расшифровка
        кода), а не само значение. Точечный аналог :meth:`object_attributes_descriptions`
        для случая, когда известен id типа атрибута. У множественного атрибута описаний
        может быть несколько, поэтому всегда список строк. Только чтение — checkout не
        нужен.

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для
                всех версий. Не идентификатор версии (``id`` / F_ID).
            attribute_id: Идентификатор ТИПА атрибута (какую характеристику читать).
            throw_not_found: Если ``True``, при отсутствии атрибута сервер вернёт ошибку
                (метод поднимет исключение); иначе метод вернёт ``None``.

        Returns:
            Список строк-описаний (возможно пустой) или ``None``, если атрибут не найден
            (и ``throw_not_found`` равно ``False``).

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404 при ``throw_not_found``).

        Example:
            async with IPSClient(config=config) as ips:
                descriptions = await ips.object_attribute_descriptions(102550, 12)
                if descriptions is not None:
                    first = descriptions[0] if descriptions else None

        Notes:
            ``operationId``: ``ObjectAttributes_GetAttributeDescriptions``. Ответ —
            result-обёртка ``StringArrayNullableResultDto`` ``{entity, isEntityPresent}``,
            разворачивается в ``list[str] | None``. См. [[ips-object-model]] (раздел
            «Атрибуты»).
        """
        params: dict[str, Any] = {"throwNotFoundException": str(throw_not_found).lower()}
        data = await self._request(
            "get",
            f"/core/api/objects/{object_id}/attributes/{attribute_id}/descriptions",
            params=params,
        )
        entity = data.get("entity") if isinstance(data, dict) else None
        return [str(item) for item in entity] if entity is not None else None
