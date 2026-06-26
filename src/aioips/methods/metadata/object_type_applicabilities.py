"""Метод получения применяемостей типа объекта (что входит в его состав)."""

from ...core import APIManager
from ...schemas.metadata import ObjectTypeApplicability


class ObjectTypeApplicabilitiesMixin(APIManager):
    """Реализует ``GET .../applicabilities/objectTypeApplicabilities/{objectTypeId}``."""

    async def object_type_applicabilities(
        self: "ObjectTypeApplicabilitiesMixin",
        object_type_id: int,
    ) -> list[ObjectTypeApplicability] | None:
        """Возвращает правила применяемости для типа объекта как РОДИТЕЛЯ состава.

        Применяемость задаёт, какие дочерние типы объектов и по каким типам связи
        допустимо включать в состав объекта данного типа (тройка тип-родителя/
        тип-связи/тип-потомка). Этот метод смотрит «сверху вниз»: для типа-родителя
        перечисляет разрешённых потомков. Ответ обёрнут в ``...ListNullableResultDto``
        (``{entity, isEntityPresent}``, ``entity`` — массив или ``null``); обёртка
        разворачивается здесь, наружу отдаётся либо список схем, либо ``None``.

        Когда применять: перед добавлением объекта в состав другого объекта — чтобы
        проверить, допустим ли потомок нужного типа и по какой связи, и какие
        ограничения (``relation_constraint_mode``, ``maximum_links``) на это наложены.
        Обратное направление («во что может входить потомок») —
        :meth:`object_type_parent_applicabilities`. ``object_type_id`` берётся из
        :meth:`object_types` или :meth:`object_type_id_by_name`.

        Args:
            object_type_id: Идентификатор типа объекта-РОДИТЕЛЯ (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` объекта/версии).

        Returns:
            Список :class:`ObjectTypeApplicability` либо ``None``, если для типа нет
            настроенных применяемостей (``isEntityPresent == false`` / ``entity == null``).
            Пустой список — применяемости настроены, но ни одна не возвращена.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                rules = await ips.object_type_applicabilities(1742)
                if rules is not None:
                    for rule in rules:
                        print(rule.child_object_type_id, rule.relation_type_id)

        Notes:
            operationId ``Metadata_GetObjectTypeApplicabilitiesById``; путь
            ``GET /core/api/metadata/applicabilities/objectTypeApplicabilities/{objectTypeId}``
            (массив ``ImsApplicabilityDto`` в обёртке). См. объектной модели IPS
            (раздел «Связи и состав»). Связанные методы:
            :meth:`object_type_parent_applicabilities`, :meth:`child_object_type_ids`,
            :meth:`has_applicability`.
        """
        path = f"/core/api/metadata/applicabilities/objectTypeApplicabilities/{object_type_id}"
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        if entity is None:
            return None
        return [ObjectTypeApplicability.model_validate(item) for item in entity]
