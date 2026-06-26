"""Метод получения GUID дочерних типов по GUID родителя и типа связи."""

from uuid import UUID

from ...core import APIManager


class ApplicabilityChildObjectTypeGuidsByGuidsMixin(APIManager):
    """Реализует ``GET .../childObjectTypes/byGuids/{parentGuid}/{relationGuid}/guids``."""

    async def applicability_child_object_type_guids_by_guids(
        self: "ApplicabilityChildObjectTypeGuidsByGuidsMixin",
        parent_object_type_guid: UUID | str,
        relation_type_guid: UUID | str,
    ) -> list[str] | None:
        """Возвращает GUID дочерних типов состава по GUID родителя и GUID типа связи.

        Полностью «безымянный» вариант: и тип-родитель, и тип связи на входе, и
        дочерние типы на выходе — переносимые между базами GUID, без локальных числовых
        id. Перечисляет типы, которые можно включить в состав объекта типа
        ``parent_object_type_guid`` по связи ``relation_type_guid``. Ответ обёрнут в
        ``GuidListNullableResultDto`` (``{entity, isEntityPresent}``); обёртка
        разворачивается здесь — наружу отдаётся список либо ``None``.

        Когда применять: в интеграциях/сравнении между базами, когда вся адресация ведётся
        по GUID и нужны лишь GUID допустимых потомков. Полные описания типов по тем же
        GUID — :meth:`applicability_child_object_types_by_guids`; вариант с числовыми id
        на выходе — :meth:`applicability_child_object_type_ids_by_guids`; аналог по
        числовым id входа — :meth:`applicability_child_object_type_guids`.

        Args:
            parent_object_type_guid: GUID типа объекта-РОДИТЕЛЯ (``ObjectType.guid`` —
                переносим между базами; id-пространство ТИПОВ объектов).
            relation_type_guid: GUID типа связи (``RelationType``; переносим между базами).

        Returns:
            Список GUID дочерних типов (строки; ``ObjectType.guid``) либо ``None``,
            если применяемостей нет (``isEntityPresent == false`` / ``entity == null``).
            Пустой список — допустимых потомков по этой связи нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                parent = "cad001c5-306c-11d8-b4e9-00304f19f545"
                relation = "11111111-2222-3333-4444-555555555555"
                guids = await ips.applicability_child_object_type_guids_by_guids(parent, relation)
                if guids:
                    print(guids)

        Notes:
            operationId
            ``Metadata_GetApplicabilityChildObjectTypeGuidsByParentGuidRelationGuid``; путь
            ``GET /core/api/metadata/applicabilities/childObjectTypes/byGuids/``
            ``{parentObjectTypeGuid}/{relationTypeGuid}/guids``
            (``GuidListNullableResultDto``). См. [[ips-object-model]] (раздел «Связи и
            состав»). Связанные методы: :meth:`applicability_child_object_type_guids`,
            :meth:`applicability_child_object_type_ids_by_guids`.
        """
        path = (
            "/core/api/metadata/applicabilities/childObjectTypes/byGuids/"
            f"{parent_object_type_guid}/{relation_type_guid}/guids"
        )
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return [str(item) for item in entity] if entity is not None else None
