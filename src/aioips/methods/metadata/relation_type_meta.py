"""Метод получения типа связи по идентификатору."""

from ...core import APIManager
from ...schemas.metadata import RelationTypeMeta


class RelationTypeMetaMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/relationTypes/{id}``."""

    async def relation_type_meta(
        self: "RelationTypeMetaMixin",
        relation_type_id: int,
    ) -> RelationTypeMeta | None:
        """Возвращает описание типа связи по его идентификатору.

        Тип связи (``RelationType``) задаёт семантику ребра между объектами: прямое
        имя (``type_name``), обратное имя (``reverse_name``) и вид связи. Его
        идентификатор — отдельное id-пространство ТИПОВ связей (не путать с
        ``RelationID`` конкретной связи между объектами). Ответ сервера обёрнут в
        ``...NullableResultDto`` (``{entity, isEntityPresent}``); обёртка
        разворачивается здесь, наружу отдаётся либо схема, либо ``None``.

        Когда применять: чтобы по известному ``id`` типа связи получить его полное
        метаописание. ``id`` берётся из :meth:`relation_types_meta`,
        :meth:`default_relation_type_id` или из поля ``default_relation`` типа
        объекта. Аналог по GUID — :meth:`relation_type_meta_by_guid`.

        Args:
            relation_type_id: Идентификатор типа связи (``RelationType`` —
                id-пространство ТИПОВ связей, не ``RelationID`` конкретной связи).

        Returns:
            Тип связи по схеме :class:`RelationTypeMeta` либо ``None``, если тип с
            таким идентификатором не найден (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                rel = await ips.relation_type_meta(501)
                if rel is not None:
                    print(rel.type_name, rel.reverse_name)

        Notes:
            operationId ``Metadata_GetRelationTypeById``; путь
            ``GET /core/api/metadata/relationTypes/{id}``.
            Связанные методы: :meth:`relation_types_meta`,
            :meth:`relation_type_meta_by_guid`.
        """
        data = await self._request("get", f"/core/api/metadata/relationTypes/{relation_type_id}")
        entity = data.get("entity") if isinstance(data, dict) else None
        return RelationTypeMeta.model_validate(entity) if entity is not None else None
