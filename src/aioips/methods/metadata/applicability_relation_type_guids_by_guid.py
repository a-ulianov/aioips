"""Метод получения GUID типов связей применяемости по GUID типа объекта."""

from uuid import UUID

from ...core import APIManager


class ApplicabilityRelationTypeGuidsByGuidMixin(APIManager):
    """Реализует ``GET .../applicabilityRelationTypes/byGuid/{objectTypeGuid}/guids``."""

    async def applicability_relation_type_guids_by_guid(
        self: "ApplicabilityRelationTypeGuidsByGuidMixin",
        object_type_guid: UUID | str,
    ) -> list[str]:
        """Возвращает GUID типов связей применяемости типа объекта, адресованного по GUID.

        Полностью «безымянный» вариант: и тип объекта на входе, и типы связи на выходе —
        переносимые между базами GUID, без локальных числовых id. Перечисляет типы
        связи (``RelationType``), по которым у типа объекта настроены применяемости.
        Ответ — голый массив строк (без обёртки ``...NullableResultDto``), поэтому метод
        всегда отдаёт список, а не ``None``.

        Когда применять: в интеграциях/сравнении между базами, когда вся адресация ведётся
        по GUID — например, чтобы затем вызвать
        :meth:`applicability_child_object_type_guids_by_guids` /
        :meth:`applicability_child_object_types_by_guids`. Возврат в id-пространстве
        связей — :meth:`applicability_relation_type_ids_by_guid`; аналог по числовому
        id типа объекта — :meth:`applicability_relation_type_guids`.

        Args:
            object_type_guid: GUID типа объекта (``ObjectType.guid`` — переносим между
                базами; id-пространство ТИПОВ объектов, не ``objectGUID`` конкретного
                объекта). Подставляется в URL как есть (``UUID`` или строка).

        Returns:
            Список GUID типов связи (строки). Пустой список — у типа нет применяемостей
            ни по одной связи (или тип с таким GUID не найден: сервер отдаёт пустую
            коллекцию, а не ошибку).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = "cad001c5-306c-11d8-b4e9-00304f19f545"
                relation_guids = await ips.applicability_relation_type_guids_by_guid(guid)
                print(relation_guids)

        Notes:
            operationId ``Metadata_GetApplicabilityRelationTypeGuidsByGuid``; путь
            ``GET /core/api/metadata/applicabilities/applicabilityRelationTypes/``
            ``byGuid/{objectTypeGuid}/guids`` (голый массив ``string``). См.
            [[ips-object-model]] (раздел «Связи и состав»). Связанные методы:
            :meth:`applicability_relation_type_guids`,
            :meth:`applicability_relation_type_ids_by_guid`.
        """
        path = (
            "/core/api/metadata/applicabilities/applicabilityRelationTypes/"
            f"byGuid/{object_type_guid}/guids"
        )
        data = await self._request("get", path)
        items = data if isinstance(data, list) else []
        return [str(item) for item in items]
