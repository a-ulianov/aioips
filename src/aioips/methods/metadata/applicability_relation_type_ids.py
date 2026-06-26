"""Метод получения id типов связей применяемости для типа объекта."""

from ...core import APIManager


class ApplicabilityRelationTypeIdsMixin(APIManager):
    """Реализует ``GET .../applicabilityRelationTypes/{objectTypeId}/ids``."""

    async def applicability_relation_type_ids(
        self: "ApplicabilityRelationTypeIdsMixin",
        object_type_id: int,
    ) -> list[int]:
        """Возвращает id типов связей, участвующих в применяемостях данного типа объекта.

        Перечисляет идентификаторы типов связи (``RelationType``), по которым у типа
        ``object_type_id`` вообще настроены применяемости — без различения, выступает
        ли он родителем или потомком. Это «алфавит связей» состава для типа. Ответ —
        голый массив целых (без обёртки ``...NullableResultDto``), поэтому метод всегда
        отдаёт список, а не ``None``.

        Когда применять: чтобы заранее узнать набор релевантных типов связи и затем
        адресно запросить потомков по конкретной связи —
        :meth:`applicability_child_object_types` /
        :meth:`applicability_child_object_type_ids`. Аналог в GUID-пространстве —
        :meth:`applicability_relation_type_guids`.

        Args:
            object_type_id: Идентификатор типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID``).

        Returns:
            Список идентификаторов типов связи (``RelationType``). Пустой список —
            у типа нет применяемостей ни по одной связи.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                relation_ids = await ips.applicability_relation_type_ids(1742)
                for rid in relation_ids:
                    children = await ips.applicability_child_object_type_ids(1742, rid)

        Notes:
            operationId ``Metadata_GetApplicabilityRelationTypeIdsById``; путь
            ``GET /core/api/metadata/applicabilities/applicabilityRelationTypes/``
            ``{objectTypeId}/ids`` (голый массив ``int``). См. [[ips-object-model]]
            (раздел «Связи и состав»). Связанный метод:
            :meth:`applicability_relation_type_guids`.
        """
        path = f"/core/api/metadata/applicabilities/applicabilityRelationTypes/{object_type_id}/ids"
        data = await self._request("get", path)
        items = data if isinstance(data, list) else []
        return [int(item) for item in items]
