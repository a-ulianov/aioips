"""Метод получения состава объекта (из чего состоит)."""

from typing import Any

from ...core import APIManager
from ...schemas.relation_queries import ObjectRelation


class ConsistFromMixin(APIManager):
    """Реализует метод ``GET /core/api/Relations/ConsistFrom`` (``Relations_ConsistFrom``)."""

    async def consist_from(
        self: "ConsistFromMixin",
        object_id: int,
        *,
        recure: bool | None = None,
        relation_type_id: int | None = None,
        object_type_id: int | None = None,
    ) -> list[ObjectRelation]:
        """Возвращает состав объекта — связи к объектам, из которых он состоит.

        Запрос «из чего состоит объект»: отдаёт рёбра состава, где переданный
        объект является родителем, а результат — его прямые (или, при
        ``recure=True``, все вложенные) потомки. Зеркальный запрос «куда объект
        входит» — :meth:`enters_in_version`. Метод относится к разделу запросов
        состава (контроллер ``/core/api/Relations/...`` с ЗАГЛАВНОЙ ``R``) и не
        совпадает с разделом ``relations`` (строчная ``r``), управляющим
        отдельными записями связей и их жизненным циклом.

        Предусловие по id-пространству (критично): ``object_id`` — это
        идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для всех версий,
        а НЕ идентификатор версии (``id`` / F_ID). Каждая запись результата
        (:class:`ObjectRelation`) также адресует потомков по ``objectID``;
        конкретную версию потомка в составе уточняет поле ``part_id``.

        Args:
            object_id: Идентификатор ОБЪЕКТА-родителя (``objectID`` / F_OBJECT_ID),
                чей состав запрашивается. Не идентификатор версии.
            recure: Если ``True`` — рекурсивный обход всего дерева состава (все
                уровни вложенности); если ``False`` или не задан — только прямые
                потомки. Передаётся в запрос лишь когда задан явно.
            relation_type_id: Фильтр по идентификатору типа связи (см.
                :meth:`relation_queries_relation_types`). Передаётся только когда задан.
            object_type_id: Фильтр по идентификатору типа объекта-потомка.
                Передаётся только когда задан.

        Returns:
            Список связей состава по схеме :class:`ObjectRelation` (родитель →
            потомок). Пустой список означает, что объект ни из чего не состоит
            (с учётом заданных фильтров).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                parts = await ips.consist_from(102550, recure=False)
                for rel in parts:
                    print(rel.object_id, rel.relation_type_id)

        Notes:
            operationId ``Relations_ConsistFrom``; путь
            ``GET /core/api/Relations/ConsistFrom`` (массив ``ObjectRelationDTO``).
            См. объектной модели IPS (раздел «Связи»).
        """
        params: dict[str, Any] = {"objectId": object_id}
        if recure is not None:
            params["recure"] = str(recure).lower()
        if relation_type_id is not None:
            params["relationTypeId"] = relation_type_id
        if object_type_id is not None:
            params["objectTypeId"] = object_type_id
        data = await self._request("get", "/core/api/Relations/ConsistFrom", params=params)
        return [ObjectRelation.model_validate(item) for item in data]
