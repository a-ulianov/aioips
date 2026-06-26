"""Метод получения связи между объектами по GUID."""

from uuid import UUID

from ...core import APIManager
from ...schemas.relations import Relation


class RelationGetByGuidMixin(APIManager):
    """Реализует ``GET /core/api/relations/byGuid/{relationGuid}``.

    operationId: ``Relations_GetRelationByGuid``.
    """

    async def relation_get_by_guid(
        self: "RelationGetByGuidMixin",
        relation_guid: UUID | str,
    ) -> Relation | None:
        """Возвращает связь между объектами по её GUID.

        GUID связи — устойчивый идентификатор, в отличие от ``RelationID``, который меняется
        после ``CheckOut``/``CheckIn`` родителя. Поэтому именно GUID следует хранить как
        долговременный ключ связи. Связь направленная: ``proj_id`` (``ObjectID`` родителя) →
        ``part_id`` (``ID`` версии потомка).

        Когда применять: предпочтительный способ повторно получить ранее найденную связь —
        GUID не протухает после правки родителя (в отличие от :meth:`relation_get` по
        числовому id). GUID берётся из поля ``guid`` любой ранее полученной :class:`Relation`.

        Args:
            relation_guid: Глобальный идентификатор связи (``UUID`` или строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Подставляется в URL как есть.

        Returns:
            Связь по схеме :class:`Relation` или ``None``, если связь не найдена
            (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                relation = await ips.relation_get_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Relations_GetRelationByGuid``; путь
            ``GET /core/api/relations/byGuid/{relationGuid}``. Ответ обёрнут в
            ``...NullableResultDto``; обёртка разворачивается здесь.
        """
        data = await self._request("get", f"/core/api/relations/byGuid/{relation_guid}")
        entity = data.get("entity") if isinstance(data, dict) else None
        return Relation.model_validate(entity) if entity is not None else None
