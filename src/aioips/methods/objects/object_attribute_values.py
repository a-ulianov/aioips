"""Метод получения значений одного атрибута объекта."""

from typing import Any

from ...core import APIManager


class ObjectAttributeValuesMixin(APIManager):
    """Реализует ``GET /objects/{objectId}/attributes/{attributeId}/values``.

    Соответствует операции ``ObjectAttributes_GetAttributeValues``.
    """

    async def object_attribute_values(
        self: "ObjectAttributeValuesMixin",
        object_id: int,
        attribute_id: int,
        *,
        throw_not_found: bool = False,
    ) -> list[Any] | None:
        """Возвращает список «сырых» значений указанного атрибута объекта.

        Когда нужны только сами значения характеристики, без метаданных атрибута (имя,
        тип, флаги) — иначе используйте :meth:`object_attribute`. Атрибут может быть
        множественным, поэтому всегда список. Значения имеют разный тип (строка, число,
        дата, ссылка) в зависимости от ``FieldTypes`` атрибута, поэтому отдаются как
        список произвольных JSON-значений. Для атрибута-ссылки (``ftObjectLink``)
        значение — это id связанного объекта.

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии. Только чтение — checkout не нужен.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для
                всех версий. Не идентификатор версии (``id`` / F_ID).
            attribute_id: Идентификатор ТИПА атрибута.
            throw_not_found: Если ``True``, при отсутствии атрибута сервер вернёт ошибку
                (метод поднимет исключение); иначе метод вернёт ``None``.

        Returns:
            Список значений атрибута (возможно пустой) или ``None``, если атрибут не
            найден (и ``throw_not_found`` равно ``False``).

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404 при ``throw_not_found``).

        Example:
            async with IPSClient(config=config) as ips:
                values = await ips.object_attribute_values(102550, 12)
                # для ftObjectLink элементы — это id связанных объектов

        Notes:
            ``operationId``: ``ObjectAttributes_GetAttributeValues``. Ответ — result-
            обёртка ``{entity, isEntityPresent}``, разворачивается в ``list | None``.
        """
        params: dict[str, Any] = {"throwNotFoundException": str(throw_not_found).lower()}
        data = await self._request(
            "get",
            f"/core/api/objects/{object_id}/attributes/{attribute_id}/values",
            params=params,
        )
        if not isinstance(data, dict):
            return None
        entity = data.get("entity")
        return list(entity) if entity is not None else None
