"""Метод получения формульных атрибутов, зависящих от атрибута (для типа объекта)."""

from ...core import APIManager


class RelatedFormulaAttributesForObjectMixin(APIManager):
    """Реализует метод формульных зависимостей атрибутов для типа объекта.

    Путь: ``GET .../relatedFormulaAttributesForObject/{objectTypeId}/{attributeTypeId}``.
    """

    async def related_formula_attributes_for_object(
        self: "RelatedFormulaAttributesForObjectMixin",
        object_type_id: int,
        attribute_type_id: int,
    ) -> list[int]:
        """Возвращает id формульных атрибутов объекта, зависящих от заданного атрибута.

        Формульный атрибут — атрибут, значение которого вычисляется по формуле от других
        атрибутов. Метод для типа объекта ``object_type_id`` перечисляет формульные
        атрибуты, чьи формулы ссылаются на атрибут ``attribute_type_id`` (то есть
        пересчитываются при его изменении). Ответ сервера — плоский массив целых, без
        обёртки ``...NullableResultDto``.

        Когда применять: чтобы оценить «волну» пересчёта при изменении значения атрибута
        у объекта данного типа (какие формульные атрибуты надо пересчитать). Аналог для
        связей — :meth:`related_formula_attributes_for_relation`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (id-пространство типов объектов
                метаданных, не id объекта/версии).
            attribute_type_id: Идентификатор исходного ТИПА атрибута, от которого ищут
                зависимости (id-пространство типов атрибутов).

        Returns:
            Список ``id`` формульных типов атрибутов (id-пространство ТИПОВ атрибутов),
            зависящих от заданного атрибута у данного типа объекта. Пустой список —
            зависимостей нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                dependents = await ips.related_formula_attributes_for_object(1742, 1029)
                print(dependents)

        Notes:
            operationId ``Metadata_GetRelatedFormulaAttributesForObject``; путь
            ``GET .../relatedFormulaAttributesForObject/{objectTypeId}/{attributeTypeId}``
            (ответ — массив ``int``). Связанные методы:
            :meth:`related_formula_attributes_for_relation`.
        """
        path = (
            "/core/api/metadata/relatedFormulaAttributesForObject/"
            f"{object_type_id}/{attribute_type_id}"
        )
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
