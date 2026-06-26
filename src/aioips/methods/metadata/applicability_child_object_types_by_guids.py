"""Метод получения дочерних типов объектов по GUID родителя и типа связи."""

from ...core import APIManager
from ...schemas.metadata import ObjectType


class ApplicabilityChildObjectTypesByGuidsMixin(APIManager):
    """Реализует ``GET .../childObjectTypes/byGuids/{parentObjectTypeGuid}/{relationTypeGuid}``."""

    async def applicability_child_object_types_by_guids(
        self: "ApplicabilityChildObjectTypesByGuidsMixin",
        parent_object_type_guid: str,
        relation_type_guid: str,
    ) -> list[ObjectType] | None:
        """Возвращает описания дочерних типов, допустимых в составе, по GUID родителя и связи.

        То же, что :meth:`applicability_child_object_types`, но и тип-родитель, и тип
        связи адресуются переносимыми между базами GUID, а не числовыми id.
        Перечисляет полные :class:`ObjectType` (имена, режим версионирования), которые
        можно включить в состав объекта типа ``parent_object_type_guid`` по связи
        ``relation_type_guid``. Ответ обёрнут в ``...ListNullableResultDto``
        (``{entity, isEntityPresent}``); обёртка разворачивается здесь.

        Когда применять: когда на руках GUID типа-родителя и GUID типа связи
        (переносимый конфиг/интеграция), а нужны человекочитаемые описания допустимых
        потомков. Аналог в id-пространстве — :meth:`applicability_child_object_types`.

        Args:
            parent_object_type_guid: GUID типа объекта-РОДИТЕЛЯ (``ObjectType.guid`` —
                переносим между базами; id-пространство ТИПОВ объектов).
            relation_type_guid: GUID типа связи (``RelationType``; переносим между базами).

        Returns:
            Список :class:`ObjectType` либо ``None``, если применяемостей нет
            (``isEntityPresent == false`` / ``entity == null``). Пустой список —
            допустимых потомков по этой связи нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                parent = "cad001c5-306c-11d8-b4e9-00304f19f545"
                relation = "11111111-2222-3333-4444-555555555555"
                types = await ips.applicability_child_object_types_by_guids(parent, relation)
                if types is not None:
                    for object_type in types:
                        print(object_type.id, object_type.object_name)

        Notes:
            operationId ``Metadata_GetApplicabilityChildObjectTypesByGuids``; путь
            ``GET /core/api/metadata/applicabilities/childObjectTypes/byGuids/``
            ``{parentObjectTypeGuid}/{relationTypeGuid}`` (массив ``ImsObjectTypeDto`` в
            обёртке). См. [[ips-object-model]] (раздел «Связи и состав»). Связанные
            методы: :meth:`applicability_child_object_types`,
            :meth:`applicability_child_object_type_guids`.
        """
        path = (
            "/core/api/metadata/applicabilities/childObjectTypes/byGuids/"
            f"{parent_object_type_guid}/{relation_type_guid}"
        )
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        if entity is None:
            return None
        return [ObjectType.model_validate(item) for item in entity]
