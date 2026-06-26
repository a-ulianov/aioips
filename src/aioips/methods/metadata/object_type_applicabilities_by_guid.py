"""Метод получения применяемостей типа объекта-родителя по GUID."""

from ...core import APIManager
from ...schemas.metadata import ObjectTypeApplicability


class ObjectTypeApplicabilitiesByGuidMixin(APIManager):
    """Реализует ``GET .../applicabilities/objectTypeApplicabilities/byGuid/{objectTypeGuid}``."""

    async def object_type_applicabilities_by_guid(
        self: "ObjectTypeApplicabilitiesByGuidMixin",
        object_type_guid: str,
    ) -> list[ObjectTypeApplicability] | None:
        """Возвращает правила применяемости типа-РОДИТЕЛЯ, заданного GUID.

        То же, что :meth:`object_type_applicabilities`, но тип-родитель адресуется
        переносимым между базами GUID типа объекта, а не числовым ``ObjectTypeID``.
        Применяемость — правило разрешённого состава: какие дочерние типы и по каким
        связям допустимо включать в состав объекта данного типа (взгляд «сверху вниз»).
        Ответ обёрнут в ``...ListNullableResultDto`` (``{entity, isEntityPresent}``,
        ``entity`` — массив или ``null``); обёртка разворачивается здесь.

        Когда применять: когда на руках GUID типа (например, из переносимого
        конфига/интеграции), а не локальный id. GUID типа берётся из поля ``guid``
        :class:`ObjectType` (это id-пространство ТИПОВ; не путать с ``guid`` версии
        или ``objectGUID`` объекта).

        Args:
            object_type_guid: GUID типа объекта-РОДИТЕЛЯ (``ObjectType.guid`` —
                переносим между базами; id-пространство ТИПОВ объектов).

        Returns:
            Список :class:`ObjectTypeApplicability` либо ``None``, если применяемостей
            нет (``isEntityPresent == false`` / ``entity == null``). Пустой список —
            применяемости настроены, но ни одна не возвращена.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = "cad001c5-306c-11d8-b4e9-00304f19f545"
                rules = await ips.object_type_applicabilities_by_guid(guid)
                if rules is not None:
                    for rule in rules:
                        print(rule.child_object_type_id, rule.relation_type_id)

        Notes:
            operationId ``Metadata_GetObjectTypeApplicabilitiesByGuid``; путь
            ``GET /core/api/metadata/applicabilities/objectTypeApplicabilities/byGuid/``
            ``{objectTypeGuid}`` (массив ``ImsApplicabilityDto`` в обёртке). См.
            [[ips-object-model]] (раздел «Связи и состав»). Связанные методы:
            :meth:`object_type_applicabilities`, :meth:`has_applicability_by_guid`.
        """
        path = (
            "/core/api/metadata/applicabilities/objectTypeApplicabilities/byGuid/"
            f"{object_type_guid}"
        )
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        if entity is None:
            return None
        return [ObjectTypeApplicability.model_validate(item) for item in entity]
