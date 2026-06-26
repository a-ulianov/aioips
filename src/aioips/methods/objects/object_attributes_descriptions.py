"""Метод получения описаний всех атрибутов объекта."""

from typing import Any

from ...core import APIManager


class ObjectAttributesDescriptionsMixin(APIManager):
    """Реализует ``ObjectAttributes_GetAttributesDescriptions`` (описания всех атрибутов)."""

    async def object_attributes_descriptions(
        self: "ObjectAttributesDescriptionsMixin",
        object_id: int,
        *,
        throw_not_found: bool = False,
    ) -> list[dict[str, Any]] | None:
        """Возвращает текстовые описания значений всех атрибутов объекта.

        Описание атрибута — это дополнительный пояснительный текст к значению
        (например, расшифровка кода или комментарий), а не само значение и не
        метаданные типа. Применяйте, когда нужны именно описания по всем атрибутам
        сразу; для описаний одного атрибута есть
        :meth:`object_attribute_descriptions`, а для значений — :meth:`object_attributes`
        / :meth:`object_attributes_values`. Только чтение — checkout не нужен.

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для
                всех версий. Не идентификатор версии (``id`` / F_ID).
            throw_not_found: Если ``True``, при отсутствии данных сервер вернёт ошибку
                (метод поднимет исключение); иначе метод вернёт ``None``.

        Returns:
            Список словарей-описаний или ``None``, если описаний нет (и
            ``throw_not_found`` равно ``False``). Каждый элемент — структура
            ``AttributeDescriptionsDto``: ключ ``attributeId`` (id типа атрибута) и
            ``descriptions`` (список строк-описаний значений атрибута). Список
            ``descriptions`` может прийти ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404 при ``throw_not_found``).

        Example:
            async with IPSClient(config=config) as ips:
                items = await ips.object_attributes_descriptions(102550)
                if items is not None:
                    by_attr = {it["attributeId"]: it["descriptions"] for it in items}

        Notes:
            ``operationId``: ``ObjectAttributes_GetAttributesDescriptions``. Ответ —
            result-обёртка ``AttributeDescriptionsDtoListNullableResultDto``
            ``{entity, isEntityPresent}``, разворачивается в ``list | None``.
            См. объектной модели IPS (раздел «Атрибуты»).
        """
        params: dict[str, Any] = {"throwNotFoundException": str(throw_not_found).lower()}
        data = await self._request(
            "get", f"/core/api/objects/{object_id}/attributesDescriptions", params=params
        )
        entity = data.get("entity") if isinstance(data, dict) else None
        return list(entity) if entity is not None else None
