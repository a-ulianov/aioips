"""Метод получения связей заданного типа связи."""

from ...core import APIManager
from ...schemas.relation_types import QuickRelationInfo


class RelationTypeRelationsMixin(APIManager):
    """Реализует ``GET /core/api/relationTypes/{relationTypeId}/relations``.

    operationId ``Relations_GetRelationsByRelationTypeId``.
    """

    async def relation_type_relations(
        self: "RelationTypeRelationsMixin",
        relation_type_id: int,
    ) -> list[QuickRelationInfo]:
        """Возвращает все связи заданного типа в краткой форме.

        Тип связи направленный: задаёт смысл отношения родитель→потомок (например,
        состав изделия). Метод перечисляет существующие экземпляры связей этого типа,
        каждый из которых соединяет объект-родитель (``proj_id`` = ``ObjectID`` родителя)
        с версией объекта-потомка (``part_id`` = ``ID`` версии потомка).

        Когда применять: для перечисления всех связей одного типа по всей базе сразу с
        ключевыми полями (родитель/потомок/guid), без точечной загрузки. В отличие от
        :meth:`relations_by_project`, не ограничивается одним родителем. Если нужны только
        идентификаторы — дешевле :meth:`relation_type_relation_ids`. ``relation_type_id``
        берётся из :meth:`relation_types`.

        Внимание: поле ``relation_id`` в возвращаемых записях нестабильно (меняется после
        ``CheckOut``/``CheckIn`` родителя) — для устойчивой идентификации связи используйте
        ``guid``.

        Args:
            relation_type_id: Идентификатор типа связи (``id`` из :meth:`relation_types`),
                чьи связи нужно получить.

        Returns:
            Список краткой информации о связях по схеме :class:`QuickRelationInfo`; пустой
            список, если связей этого типа нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                relations = await ips.relation_type_relations(1)
                parents = {rel.proj_id for rel in relations}

        Notes:
            operationId ``Relations_GetRelationsByRelationTypeId``; путь
            ``GET /core/api/relationTypes/{relationTypeId}/relations``.
        """
        path = f"/core/api/relationTypes/{relation_type_id}/relations"
        data = await self._request("get", path)
        return [QuickRelationInfo.model_validate(item) for item in data]
