"""Метод получения применяемостей типа объекта (во что он может входить)."""

from ...core import APIManager
from ...schemas.metadata import ObjectTypeApplicability


class ObjectTypeParentApplicabilitiesMixin(APIManager):
    """Реализует ``GET .../applicabilities/objectTypeParentApplicabilities/{partTypeId}``."""

    async def object_type_parent_applicabilities(
        self: "ObjectTypeParentApplicabilitiesMixin",
        part_type_id: int,
    ) -> list[ObjectTypeApplicability] | None:
        """Возвращает правила применяемости для типа объекта как ПОТОМКА состава.

        Применяемость задаёт тройку (тип-родителя/тип-связи/тип-потомка). Этот метод
        смотрит «снизу вверх»: для типа-потомка перечисляет, в какие родительские типы
        и по каким типам связи он может входить. Ответ обёрнут в
        ``...ListNullableResultDto`` (``{entity, isEntityPresent}``, ``entity`` — массив
        или ``null``); обёртка разворачивается здесь, наружу отдаётся либо список схем,
        либо ``None``.

        Когда применять: чтобы выяснить допустимых родителей для объекта данного типа
        (например, при построении дерева состава или валидации «куда можно поместить»).
        Обратное направление («что может входить в родителя») —
        :meth:`object_type_applicabilities`. ``part_type_id`` берётся из
        :meth:`object_types` или :meth:`object_type_id_by_name`.

        Args:
            part_type_id: Идентификатор типа объекта-ПОТОМКА (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` объекта/версии).

        Returns:
            Список :class:`ObjectTypeApplicability` либо ``None``, если для типа нет
            родительских применяемостей (``isEntityPresent == false`` / ``entity == null``).
            Пустой список — применяемости настроены, но ни одна не возвращена.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                rules = await ips.object_type_parent_applicabilities(1755)
                if rules is not None:
                    for rule in rules:
                        print(rule.in_object_type_id, rule.relation_type_id)

        Notes:
            operationId ``Metadata_GetObjectTypeParentApplicabilities``; путь
            ``GET /core/api/metadata/applicabilities/objectTypeParentApplicabilities/{partTypeId}``
            (массив ``ImsApplicabilityDto`` в обёртке). См. [[ips-object-model]]
            (раздел «Связи и состав»). Связанные методы:
            :meth:`object_type_applicabilities`, :meth:`has_applicability`.
        """
        path = f"/core/api/metadata/applicabilities/objectTypeParentApplicabilities/{part_type_id}"
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        if entity is None:
            return None
        return [ObjectTypeApplicability.model_validate(item) for item in entity]
