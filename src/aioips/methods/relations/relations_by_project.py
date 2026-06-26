"""Метод получения связей родителя по типу связи."""

from ...core import APIManager
from ...schemas.relations import Relation


class RelationsByProjectMixin(APIManager):
    """Реализует ``GET /core/api/relations/projects/{projectId}/relationTypes/{relationTypeId}``."""

    async def relations_by_project(
        self: "RelationsByProjectMixin",
        project_id: int,
        relation_type_id: int,
    ) -> list[Relation]:
        """Возвращает связи объекта-родителя указанного типа.

        Это основной способ читать состав изделия: по объекту-родителю и типу связи
        получить все исходящие связи к потомкам. ``project_id`` здесь — это ``ProjID``,
        то есть ``ObjectID`` объекта-родителя (общий для всех его версий), а не идентификатор
        версии. У каждой возвращённой связи ``part_id`` — это ``ID`` версии объекта-потомка.

        Когда применять: чтобы развернуть состав/связи конкретного родителя одного типа
        (в отличие от :meth:`relation_type_relations`, которая отдаёт ВСЕ связи типа по
        всей базе). ``relation_type_id`` берётся из :meth:`relation_types`.

        Предусловие по id-пространствам: ``project_id`` = ``ObjectID`` родителя (F_OBJECT_ID),
        а возвращаемый ``part_id`` = ``ID`` версии потомка (F_ID). ``part_id`` нельзя подавать
        в ``object_get`` напрямую — тому нужен ``ObjectID``; для объекта-потомка используйте
        поле ``part_object_id`` связи (если оно не ``0``).

        Args:
            project_id: Идентификатор объекта-родителя (``ProjID`` = ``ObjectID`` родителя,
                общий для всех версий), не идентификатор версии.
            relation_type_id: Идентификатор типа связи (``id`` из :meth:`relation_types`),
                по которому отбираются связи.

        Returns:
            Список связей по схеме :class:`Relation`; пустой список, если связей нет (а
            также при неожиданной не-списочной форме ответа сервера).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                relations = await ips.relations_by_project(
                    project_id=5005, relation_type_id=1
                )
                child_version_ids = [r.part_id for r in relations]

        Notes:
            operationId ``Relations_GetRelationsByProject``; путь
            ``GET /core/api/relations/projects/{projectId}/relationTypes/{relationTypeId}``.
            Имя ``projectId`` в пути вводит в заблуждение — фактически принимает ``ObjectID``
            родителя (см. объектной модели IPS).
        """
        data = await self._request(
            "get",
            f"/core/api/relations/projects/{project_id}/relationTypes/{relation_type_id}",
        )
        items = data if isinstance(data, list) else []
        return [Relation.model_validate(item) for item in items]
