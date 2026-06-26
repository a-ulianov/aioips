"""Метод получения связи по проекту (родителю) и потомку (версии)."""

from ...core import APIManager
from ...schemas.relations import Relation


class RelationByProjectAndPartMixin(APIManager):
    """Реализует ``Relations_GetRelationByProjectIdAndPartId`` (связь по родителю + потомку)."""

    async def relation_by_project_and_part(
        self: "RelationByProjectAndPartMixin",
        project_id: int,
        part_id: int,
    ) -> Relation | None:
        """Возвращает связь по паре «объект-родитель → версия-потомок».

        Поиск связи по её естественным концам, без знания ``relationID``: задаются проект
        (родитель) и потомок. Применяйте, когда известно, какой объект входит в состав
        какого, и нужна сама запись связи (тип, дата, GUID). Для устойчивой адресации по
        ключу есть :meth:`relation_by_guid_and_project`; для перебора состава —
        раздел ``relation_queries`` (:meth:`consist_from`, :meth:`enters_in_version`).
        Только чтение — checkout не нужен.

        ⚠️ Разные id-пространства концов связи (см. объектной модели IPS):
        ``project_id`` — это ``ObjectID`` РОДИТЕЛЯ (``ProjID``), общий для всех его версий;
        ``part_id`` — это ``ID`` ВЕРСИИ ПОТОМКА (``PartID``), идентификатор конкретной
        версии, а не объекта. Перепутав их местами или передав id объекта вместо id версии
        потомка, вы не найдёте связь.

        Args:
            project_id: Идентификатор ОБЪЕКТА-РОДИТЕЛЯ (``ObjectID`` / ``ProjID`` связи),
                общий для всех версий родителя.
            part_id: Идентификатор ВЕРСИИ объекта-потомка (``ID`` / ``PartID`` связи),
                идентификатор конкретной версии, а не объекта.

        Returns:
            Связь по схеме :class:`Relation` или ``None``, если связь не найдена
            (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                relation = await ips.relation_by_project_and_part(102550, 700321)
                if relation is not None:
                    print(relation.relation_id, relation.relation_type)

        Notes:
            ``operationId``: ``Relations_GetRelationByProjectIdAndPartId``; путь
            ``GET /core/api/relations/projects/{projectId}/parts/{partId}``. Ответ обёрнут
            в ``RelationDtoNullableResultDto`` ``{entity, isEntityPresent}`` — обёртка
            разворачивается здесь. См. объектной модели IPS (раздел «Связи и состав»).
        """
        data = await self._request(
            "get",
            f"/core/api/relations/projects/{project_id}/parts/{part_id}",
        )
        entity = data.get("entity") if isinstance(data, dict) else None
        return Relation.model_validate(entity) if entity is not None else None
