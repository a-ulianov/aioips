"""Метод получения id дочерних типов по GUID родителя и типа связи."""

from uuid import UUID

from ...core import APIManager


class ApplicabilityChildObjectTypeIdsByGuidsMixin(APIManager):
    """Реализует ``GET .../childObjectTypes/byGuids/{parentGuid}/{relationGuid}/ids``."""

    async def applicability_child_object_type_ids_by_guids(
        self: "ApplicabilityChildObjectTypeIdsByGuidsMixin",
        parent_object_type_guid: UUID | str,
        relation_type_guid: UUID | str,
    ) -> list[int] | None:
        """Возвращает id дочерних типов состава по GUID родителя и GUID типа связи.

        То же, что :meth:`applicability_child_object_type_ids`, но и тип-родитель, и тип
        связи адресуются переносимыми между базами GUID, а не числовыми id. Плоский
        список идентификаторов ТИПОВ объектов, которые можно включить в состав объекта
        типа ``parent_object_type_guid`` по связи ``relation_type_guid``. Ответ обёрнут
        в ``Int32ListNullableResultDto`` (``{entity, isEntityPresent}``); обёртка
        разворачивается здесь — наружу отдаётся список либо ``None``.

        Когда применять: когда на руках GUID типа-родителя и GUID типа связи (переносимый
        конфиг/интеграция), а нужны лишь числовые id допустимых потомков (фильтрация
        кандидатов на добавление в состав). Полные описания типов по тем же GUID —
        :meth:`applicability_child_object_types_by_guids`; вариант с GUID на выходе —
        :meth:`applicability_child_object_type_guids_by_guids`; аналог по числовым id —
        :meth:`applicability_child_object_type_ids`.

        Args:
            parent_object_type_guid: GUID типа объекта-РОДИТЕЛЯ (``ObjectType.guid`` —
                переносим между базами; id-пространство ТИПОВ объектов).
            relation_type_guid: GUID типа связи (``RelationType``; переносим между базами).

        Returns:
            Список идентификаторов дочерних типов (``ObjectTypeID``) либо ``None``,
            если применяемостей нет (``isEntityPresent == false`` / ``entity == null``).
            Пустой список — допустимых потомков по этой связи нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                parent = "cad001c5-306c-11d8-b4e9-00304f19f545"
                relation = "11111111-2222-3333-4444-555555555555"
                ids = await ips.applicability_child_object_type_ids_by_guids(parent, relation)
                if ids:
                    print(ids)

        Notes:
            operationId
            ``Metadata_GetApplicabilityChildObjectTypeIdsByParentGuidRelationGuid``; путь
            ``GET /core/api/metadata/applicabilities/childObjectTypes/byGuids/``
            ``{parentObjectTypeGuid}/{relationTypeGuid}/ids``
            (``Int32ListNullableResultDto``). См. объектной модели IPS (раздел «Связи и
            состав»). Связанные методы: :meth:`applicability_child_object_type_ids`,
            :meth:`applicability_child_object_type_guids_by_guids`.
        """
        path = (
            "/core/api/metadata/applicabilities/childObjectTypes/byGuids/"
            f"{parent_object_type_guid}/{relation_type_guid}/ids"
        )
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return [int(item) for item in entity] if entity is not None else None
