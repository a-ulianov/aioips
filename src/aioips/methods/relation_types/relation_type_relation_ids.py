"""Метод получения идентификаторов связей заданного типа связи."""

from ...core import APIManager


class RelationTypeRelationIdsMixin(APIManager):
    """Реализует ``GET /core/api/relationTypes/{relationTypeId}/relationIds``.

    operationId ``Relations_GetRelationIdsByRelationTypeId``.
    """

    async def relation_type_relation_ids(
        self: "RelationTypeRelationIdsMixin",
        relation_type_id: int,
    ) -> list[int]:
        """Возвращает идентификаторы всех связей заданного типа.

        Лёгкая разновидность :meth:`relation_type_relations`: отдаёт только идентификаторы
        связей указанного типа, без сопутствующих сведений о родителе и потомке. Подходит,
        когда нужен лишь перечень связей для последующей точечной загрузки.

        Когда применять: для дешёвого перечисления связей типа по всей базе, когда детали
        (родитель/потомок) не нужны сразу; каждый id затем разворачивается через
        :meth:`relation_get`. Если детали нужны сразу — берите :meth:`relation_type_relations`.
        ``relation_type_id`` берётся из :meth:`relation_types`.

        Внимание: идентификаторы связей нестабильны — они меняются после ``CheckOut`` или
        ``CheckIn`` объекта-родителя, поэтому их не следует кэшировать между операциями
        (для долговременного ключа берите GUID связи).

        Args:
            relation_type_id: Идентификатор типа связи (``id`` из :meth:`relation_types`),
                чьи связи нужно получить.

        Returns:
            Список идентификаторов связей (``RelationID``); пустой список, если связей
            этого типа нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                relation_ids = await ips.relation_type_relation_ids(1)
                print(len(relation_ids))

        Notes:
            operationId ``Relations_GetRelationIdsByRelationTypeId``; путь
            ``GET /core/api/relationTypes/{relationTypeId}/relationIds``.
        """
        path = f"/core/api/relationTypes/{relation_type_id}/relationIds"
        data = await self._request("get", path)
        return [int(item) for item in data]
