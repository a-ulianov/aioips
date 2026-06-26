"""Метод получения значений одного атрибута связи."""

from typing import Any

from ...core import APIManager


class RelationAttributeValuesMixin(APIManager):
    """Реализует ``GET /relations/{relationId}/attributes/{attributeId}/values``.

    Соответствует операции ``RelationAttributes_GetAttributeValues``.
    """

    async def relation_attribute_values(
        self: "RelationAttributeValuesMixin",
        relation_id: int,
        attribute_id: int,
        *,
        throw_not_found: bool = False,
    ) -> list[Any] | None:
        """Возвращает список «сырых» значений указанного атрибута СВЯЗИ.

        Когда нужны только сами значения характеристики связи, без метаданных атрибута
        (имя, тип, флаги) — иначе используйте :meth:`relation_attribute`. Связь —
        атрибутируемая сущность (``IDBAttributable``), её атрибут может быть множественным,
        поэтому всегда список. Значения имеют разный тип (строка, число, дата, ссылка) в
        зависимости от ``FieldTypes`` атрибута, поэтому отдаются как список произвольных
        JSON-значений; для атрибута-ссылки (``ftObjectLink``) значение — id связанного
        объекта. Отличие от :meth:`object_attribute_values`: тот читает значения атрибута
        ОБЪЕКТА по ``objectID``, а здесь — атрибута СВЯЗИ по ``relationID``. Только чтение —
        checkout не нужен.

        Args:
            relation_id: Идентификатор СВЯЗИ (``relationID``, отдельное id-пространство
                связей). ⚠️ ``relationID`` нестабилен: меняется после ``CheckOut``/
                ``CheckIn`` родителя — не кэшируйте его (см. объектной модели IPS).
            attribute_id: Идентификатор ТИПА атрибута.
            throw_not_found: Если ``True``, при отсутствии атрибута сервер вернёт ошибку
                (метод поднимет исключение); иначе метод вернёт ``None``.

        Returns:
            Список значений атрибута связи (возможно пустой) или ``None``, если атрибут не
            найден (и ``throw_not_found`` равно ``False``).

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404 при ``throw_not_found``).

        Example:
            async with IPSClient(config=config) as ips:
                values = await ips.relation_attribute_values(700123, 12)
                # для ftObjectLink элементы — это id связанных объектов

        Notes:
            ``operationId``: ``RelationAttributes_GetAttributeValues``. Ответ — обёртка
            ``ObjectArrayNullableResultDto`` ``{entity, isEntityPresent}``,
            разворачивается в ``list | None``.
        """
        params: dict[str, Any] = {"throwNotFoundException": str(throw_not_found).lower()}
        data = await self._request(
            "get",
            f"/core/api/relations/{relation_id}/attributes/{attribute_id}/values",
            params=params,
        )
        if not isinstance(data, dict):
            return None
        entity = data.get("entity")
        return list(entity) if entity is not None else None
