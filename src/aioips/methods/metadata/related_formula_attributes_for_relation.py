"""Метод получения формульных атрибутов, зависящих от атрибута (для типа связи)."""

from ...core import APIManager


class RelatedFormulaAttributesForRelationMixin(APIManager):
    """Реализует метод формульных зависимостей атрибутов для типа связи.

    Путь: ``GET .../relatedFormulaAttributesForRelation/{relationTypeId}/{attributeTypeId}``.
    """

    async def related_formula_attributes_for_relation(
        self: "RelatedFormulaAttributesForRelationMixin",
        relation_type_id: int,
        attribute_type_id: int,
    ) -> list[int]:
        """Возвращает id формульных атрибутов связи, зависящих от заданного атрибута.

        Аналог :meth:`related_formula_attributes_for_object`, но для атрибутов ТИПА СВЯЗИ.
        Для типа связи ``relation_type_id`` перечисляет формульные атрибуты, чьи формулы
        ссылаются на атрибут ``attribute_type_id`` (пересчитываются при его изменении).
        Ответ сервера — плоский массив целых, без обёртки ``...NullableResultDto``.

        Когда применять: чтобы оценить «волну» пересчёта формульных атрибутов связи при
        изменении значения исходного атрибута. Аналог для объектов —
        :meth:`related_formula_attributes_for_object`.

        Args:
            relation_type_id: Идентификатор ТИПА связи (``RelationType``; id-пространство
                типов связей метаданных, не конкретная связь).
            attribute_type_id: Идентификатор исходного ТИПА атрибута, от которого ищут
                зависимости (id-пространство типов атрибутов).

        Returns:
            Список ``id`` формульных типов атрибутов (id-пространство ТИПОВ атрибутов),
            зависящих от заданного атрибута у данного типа связи. Пустой список —
            зависимостей нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                dependents = await ips.related_formula_attributes_for_relation(7, 1029)
                print(dependents)

        Notes:
            operationId ``Metadata_GetRelatedFormulaAttributesForRelation``; путь
            ``GET .../relatedFormulaAttributesForRelation/{relationTypeId}/{attributeTypeId}``
            (ответ — массив ``int``). Связанные методы:
            :meth:`related_formula_attributes_for_object`.
        """
        path = (
            "/core/api/metadata/relatedFormulaAttributesForRelation/"
            f"{relation_type_id}/{attribute_type_id}"
        )
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
