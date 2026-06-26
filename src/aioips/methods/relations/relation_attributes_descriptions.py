"""Метод получения описаний всех атрибутов связи."""

from typing import Any

from ...core import APIManager


class RelationAttributesDescriptionsMixin(APIManager):
    """Реализует ``RelationAttributes_GetAttributesDescriptions`` (описания атрибутов связи)."""

    async def relation_attributes_descriptions(
        self: "RelationAttributesDescriptionsMixin",
        relation_id: int,
    ) -> list[Any] | None:
        """Возвращает текстовые описания значений всех атрибутов СВЯЗИ.

        Описание атрибута — дополнительный пояснительный текст к значению (например,
        расшифровка кода или комментарий), а не само значение и не метаданные типа.
        Применяйте, когда нужны именно описания по всем атрибутам связи сразу; для описаний
        одного атрибута есть :meth:`relation_attribute_descriptions`, а для значений —
        :meth:`relation_attributes` / :meth:`relation_attributes_values`. Отличие от
        :meth:`object_attributes_descriptions`: тот читает описания атрибутов ОБЪЕКТА по
        ``objectID``, а здесь — атрибутов СВЯЗИ по ``relationID``. Только чтение —
        checkout не нужен.

        Args:
            relation_id: Идентификатор СВЯЗИ (``relationID``, отдельное id-пространство
                связей). ⚠️ ``relationID`` нестабилен: меняется после ``CheckOut``/
                ``CheckIn`` родителя — не кэшируйте его (см. [[ips-object-model]]).

        Returns:
            Список элементов-описаний или ``None``, если описаний нет
            (``isEntityPresent == false``). Каждый элемент — структура
            ``AttributeDescriptionsDto`` с полями ``attributeId`` (id типа атрибута) и
            ``descriptions`` (список строк-описаний значений атрибута; может прийти
            ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                items = await ips.relation_attributes_descriptions(700123)
                if items is not None:
                    by_attr = {it["attributeId"]: it["descriptions"] for it in items}

        Notes:
            ``operationId``: ``RelationAttributes_GetAttributesDescriptions``; путь
            ``GET /core/api/relations/{relationId}/attributesDescriptions``. Ответ —
            result-обёртка ``AttributeDescriptionsDtoListNullableResultDto``
            ``{entity, isEntityPresent}``, разворачивается в ``list | None``. Навигация по
            составу — раздел ``relation_queries``. См. [[ips-object-model]]
            (раздел «Атрибуты»).
        """
        data = await self._request(
            "get",
            f"/core/api/relations/{relation_id}/attributesDescriptions",
        )
        entity = data.get("entity") if isinstance(data, dict) else None
        return list(entity) if entity is not None else None
