"""Метод получения связи по GUID связи и проекту (объекту-родителю)."""

from ...core import APIManager
from ...schemas.relations import Relation


class RelationByGuidAndProjectMixin(APIManager):
    """Реализует ``Relations_GetRelationByGuidAndProjectId`` (связь по GUID + проекту)."""

    async def relation_by_guid_and_project(
        self: "RelationByGuidAndProjectMixin",
        relation_guid: str,
        project_id: int,
    ) -> Relation | None:
        """Возвращает связь по её устойчивому ``GUID`` в контексте проекта-родителя.

        Устойчивая адресация связи: в отличие от :meth:`relation_get` (числовой
        ``relationID`` нестабилен — протухает после ``CheckOut``/``CheckIn`` родителя),
        связь ищется по ``GUID`` (постоянный ключ) внутри конкретного проекта. Применяйте,
        когда ключ связи хранится долговременно (между сессиями редактирования). Если же
        нужен поиск по паре «родитель + потомок», используйте
        :meth:`relation_by_project_and_part`. Только чтение — checkout не нужен.

        Предусловие по id-пространству: ``project_id`` — это ``ObjectID`` объекта-родителя
        (``ProjID`` связи), общий для всех его версий, а НЕ ``id`` версии.

        Args:
            relation_guid: Глобальный идентификатор связи (``GUID``, устойчивый ключ).
                Формат — строковый UUID (например ``"cad00021-306c-11d8-b4e9-..."``).
            project_id: Идентификатор ОБЪЕКТА-РОДИТЕЛЯ (``ObjectID`` / ``ProjID`` связи),
                общий для всех версий. Не идентификатор версии (``id`` / ``PartID``).

        Returns:
            Связь по схеме :class:`Relation` или ``None``, если связь не найдена
            (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                relation = await ips.relation_by_guid_and_project(
                    "cad00021-306c-11d8-b4e9-00304f19f545", 102550
                )
                if relation is not None:
                    print(relation.part_id, relation.relation_type)

        Notes:
            ``operationId``: ``Relations_GetRelationByGuidAndProjectId``; путь
            ``GET /core/api/relations/byGuid/{relationGuid}/projects/{projectId}``. Ответ
            обёрнут в ``RelationDtoNullableResultDto`` ``{entity, isEntityPresent}`` —
            обёртка разворачивается здесь. Запросы навигации по составу — в разделе
            ``relation_queries``. См. объектной модели IPS (раздел «Связи и состав»).
        """
        data = await self._request(
            "get",
            f"/core/api/relations/byGuid/{relation_guid}/projects/{project_id}",
        )
        entity = data.get("entity") if isinstance(data, dict) else None
        return Relation.model_validate(entity) if entity is not None else None
