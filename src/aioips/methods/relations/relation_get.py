"""Метод получения связи между объектами по идентификатору."""

from ...core import APIManager
from ...schemas.relations import Relation


class RelationGetMixin(APIManager):
    """Реализует метод ``GET /core/api/relations/{relationId}`` (``Relations_GetRelation``)."""

    async def relation_get(self: "RelationGetMixin", relation_id: int) -> Relation | None:
        """Возвращает связь между объектами по её идентификатору.

        Связь направленная: родитель (``proj_id`` — ``ObjectID`` объекта-родителя) → потомок
        (``part_id`` — ``ID`` версии объекта-потомка). Идентификатор связи нестабилен:
        он меняется после ``CheckOut``/``CheckIn`` родителя, поэтому не кэшируйте его и не
        используйте как долговременный ключ — для устойчивой идентификации берите ``guid``
        связи или тройку (``proj_id``, ``part_id``, ``relation_type``).

        Когда применять: когда уже есть свежий ``relationID`` (например, из
        :meth:`relations_by_project` или :meth:`relation_type_relation_ids`) и нужна полная
        запись связи. Если ключ хранится долговременно — берите GUID и вызывайте
        :meth:`relation_get_by_guid` (числовой id протухает после правки родителя).

        Args:
            relation_id: Идентификатор связи (``RelationID``, отдельное id-пространство
                связей; нестабилен между сессиями редактирования родителя).

        Returns:
            Связь по схеме :class:`Relation` или ``None``, если связь не найдена
            (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                relation = await ips.relation_get(700123)
                if relation is not None:
                    print(relation.proj_id, relation.part_id, relation.relation_type)

        Notes:
            operationId ``Relations_GetRelation``; путь
            ``GET /core/api/relations/{relationId}``. Ответ обёрнут в
            ``...NullableResultDto``; обёртка разворачивается здесь.
        """
        data = await self._request("get", f"/core/api/relations/{relation_id}")
        entity = data.get("entity") if isinstance(data, dict) else None
        return Relation.model_validate(entity) if entity is not None else None
