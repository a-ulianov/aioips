"""Метод получения id дочерних типов по id родителя и типа связи."""

from ...core import APIManager


class ApplicabilityChildObjectTypeIdsMixin(APIManager):
    """Реализует ``GET .../childObjectTypes/byIds/{parentObjectTypeId}/{relationTypeId}/ids``."""

    async def applicability_child_object_type_ids(
        self: "ApplicabilityChildObjectTypeIdsMixin",
        parent_object_type_id: int,
        relation_type_id: int,
    ) -> list[int] | None:
        """Возвращает id дочерних типов, допустимых в составе родителя по одной связи.

        Плоский список идентификаторов ТИПОВ объектов, которые можно включить в состав
        объекта типа ``parent_object_type_id`` по связи ``relation_type_id``. Лёгкий
        аналог :meth:`applicability_child_object_types` (там — полные
        :class:`ObjectType`). В отличие от :meth:`child_object_type_ids` (POST, список
        связей телом, opId ``...ByParentIdRelationIds``) — здесь одна связь в пути,
        метод ``GET`` (opId ``...ByParentIdRelationId``). Ответ обёрнут в
        ``Int32ListNullableResultDto`` (``{entity, isEntityPresent}``); обёртка
        разворачивается здесь.

        Когда применять: когда нужен только перечень допустимых дочерних id (фильтрация
        кандидатов на добавление в состав по конкретной связи) и не нужны имена.
        Аналог в GUID-пространстве — :meth:`applicability_child_object_type_guids`.

        Args:
            parent_object_type_id: Идентификатор типа объекта-РОДИТЕЛЯ
                (``ObjectTypeID`` — id-пространство ТИПОВ объектов, не ``ObjectID``/``ID``).
            relation_type_id: Идентификатор типа связи (``RelationType``).

        Returns:
            Список идентификаторов дочерних типов (``ObjectTypeID``) либо ``None``,
            если применяемостей нет (``isEntityPresent == false`` / ``entity == null``).
            Пустой список — допустимых потомков по этой связи нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.applicability_child_object_type_ids(1742, 501)
                if ids:
                    print(ids)

        Notes:
            operationId ``Metadata_GetApplicabilityChildObjectTypeIdsByParentIdRelationId``;
            путь ``GET /core/api/metadata/applicabilities/childObjectTypes/byIds/``
            ``{parentObjectTypeId}/{relationTypeId}/ids`` (``Int32ListNullableResultDto``).
            См. объектной модели IPS (раздел «Связи и состав»). Связанные методы:
            :meth:`applicability_child_object_types`,
            :meth:`applicability_child_object_type_guids`.
        """
        path = (
            "/core/api/metadata/applicabilities/childObjectTypes/byIds/"
            f"{parent_object_type_id}/{relation_type_id}/ids"
        )
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return list(entity) if entity is not None else None
