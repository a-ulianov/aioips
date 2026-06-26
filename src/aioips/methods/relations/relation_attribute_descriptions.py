"""Метод получения описаний одного атрибута связи."""

from ...core import APIManager


class RelationAttributeDescriptionsMixin(APIManager):
    """Реализует ``RelationAttributes_GetAttributeDescriptions`` (описания атрибута связи)."""

    async def relation_attribute_descriptions(
        self: "RelationAttributeDescriptionsMixin",
        relation_id: int,
        attribute_id: int,
    ) -> list[str] | None:
        """Возвращает текстовые описания значений одного атрибута СВЯЗИ.

        Описание — пояснительный текст к значению атрибута (например, расшифровка кода), а
        не само значение. Точечный аналог :meth:`relation_attributes_descriptions` для
        случая, когда известен id типа атрибута. У множественного атрибута описаний может
        быть несколько, поэтому всегда список строк. Отличие от
        :meth:`object_attribute_descriptions`: тот читает описания атрибута ОБЪЕКТА по
        ``objectID``, а здесь — атрибута СВЯЗИ по ``relationID``. Только чтение —
        checkout не нужен.

        Args:
            relation_id: Идентификатор СВЯЗИ (``relationID``, отдельное id-пространство
                связей). ⚠️ ``relationID`` нестабилен: меняется после ``CheckOut``/
                ``CheckIn`` родителя — не кэшируйте его (см. [[ips-object-model]]).
            attribute_id: Идентификатор ТИПА атрибута (какую характеристику читать).

        Returns:
            Список строк-описаний (возможно пустой) или ``None``, если атрибут не найден
            (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                descriptions = await ips.relation_attribute_descriptions(700123, 12)
                if descriptions is not None:
                    first = descriptions[0] if descriptions else None

        Notes:
            ``operationId``: ``RelationAttributes_GetAttributeDescriptions``; путь
            ``GET /core/api/relations/{relationId}/attributes/{attributeId}/descriptions``.
            Ответ — result-обёртка ``StringArrayNullableResultDto``
            ``{entity, isEntityPresent}`` (массив строк), разворачивается в
            ``list[str] | None``. Навигация по составу — раздел ``relation_queries``.
            См. [[ips-object-model]] (раздел «Атрибуты»).
        """
        data = await self._request(
            "get",
            f"/core/api/relations/{relation_id}/attributes/{attribute_id}/descriptions",
        )
        entity = data.get("entity") if isinstance(data, dict) else None
        return [str(item) for item in entity] if entity is not None else None
