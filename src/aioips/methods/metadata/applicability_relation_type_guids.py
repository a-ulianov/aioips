"""Метод получения GUID типов связей применяемости для типа объекта."""

from ...core import APIManager


class ApplicabilityRelationTypeGuidsMixin(APIManager):
    """Реализует ``GET .../applicabilityRelationTypes/{objectTypeId}/guids``."""

    async def applicability_relation_type_guids(
        self: "ApplicabilityRelationTypeGuidsMixin",
        object_type_id: int,
    ) -> list[str]:
        """Возвращает GUID типов связей, участвующих в применяемостях данного типа объекта.

        То же, что :meth:`applicability_relation_type_ids`, но возвращает переносимые
        между базами GUID типов связи вместо локальных числовых id. Перечисляет типы
        связи (``RelationType``), по которым у типа ``object_type_id`` настроены
        применяемости. Ответ — голый массив строк (без обёртки
        ``...NullableResultDto``), поэтому метод всегда отдаёт список, а не ``None``.

        Когда применять: когда дальнейшая логика оперирует переносимыми GUID связей
        (интеграции, сравнение между базами) — например, чтобы затем вызвать
        :meth:`applicability_child_object_types_by_guids`. Аналог в id-пространстве —
        :meth:`applicability_relation_type_ids`.

        Args:
            object_type_id: Идентификатор типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID``).

        Returns:
            Список GUID типов связи (строки). Пустой список — у типа нет
            применяемостей ни по одной связи.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                relation_guids = await ips.applicability_relation_type_guids(1742)
                print(relation_guids)

        Notes:
            operationId ``Metadata_GetApplicabilityRelationTypeGuidsById``; путь
            ``GET /core/api/metadata/applicabilities/applicabilityRelationTypes/``
            ``{objectTypeId}/guids`` (голый массив ``string``). См. [[ips-object-model]]
            (раздел «Связи и состав»). Связанный метод:
            :meth:`applicability_relation_type_ids`.
        """
        path = (
            f"/core/api/metadata/applicabilities/applicabilityRelationTypes/{object_type_id}/guids"
        )
        data = await self._request("get", path)
        items = data if isinstance(data, list) else []
        return [str(item) for item in items]
