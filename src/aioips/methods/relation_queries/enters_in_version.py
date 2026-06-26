"""Метод получения вхождений объекта (куда объект входит)."""

from typing import Any

from ...core import APIManager
from ...schemas.relation_queries import ObjectRelation


class EntersInVersionMixin(APIManager):
    """Реализует ``GET /core/api/Relations/EntersInVersion`` (``Relations_EntersInVersion``)."""

    async def enters_in_version(
        self: "EntersInVersionMixin",
        object_id: int,
        *,
        recure: bool | None = None,
        relation_type_id: int | None = None,
    ) -> list[ObjectRelation]:
        """Возвращает вхождения объекта — связи к объектам, в состав которых он входит.

        Запрос «куда объект входит»: отдаёт рёбра состава, где переданный объект
        является потомком, а результат — его прямые (или, при ``recure=True``, все
        вышестоящие) родители. Зеркальный запрос «из чего состоит» —
        :meth:`consist_from`. Метод относится к разделу запросов состава
        (контроллер ``/core/api/Relations/...`` с ЗАГЛАВНОЙ ``R``) и не совпадает
        с разделом ``relations`` (строчная ``r``), управляющим отдельными записями
        связей и их жизненным циклом.

        Предусловие по id-пространству (критично): ``object_id`` — это
        идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для всех версий,
        а НЕ идентификатор версии (``id`` / F_ID). В записях результата
        (:class:`ObjectRelation`) родитель адресуется полем ``parent_object_id``.

        Args:
            object_id: Идентификатор ОБЪЕКТА-потомка (``objectID`` / F_OBJECT_ID),
                вхождения которого запрашиваются. Не идентификатор версии.
            recure: Если ``True`` — рекурсивный обход вверх по всем уровням
                вхождения; если ``False`` или не задан — только прямые родители.
                Передаётся в запрос лишь когда задан явно.
            relation_type_id: Фильтр по идентификатору типа связи (см.
                :meth:`relation_queries_relation_types`). Передаётся только когда задан.

        Returns:
            Список связей вхождения по схеме :class:`ObjectRelation` (родитель →
            потомок, где потомок — переданный объект). Пустой список означает, что
            объект никуда не входит (с учётом заданных фильтров).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                parents = await ips.enters_in_version(102550, recure=True)
                for rel in parents:
                    print(rel.parent_object_id, rel.relation_type_id)

        Notes:
            operationId ``Relations_EntersInVersion``; путь
            ``GET /core/api/Relations/EntersInVersion`` (массив ``ObjectRelationDTO``).
            См. объектной модели IPS (раздел «Связи»).
        """
        params: dict[str, Any] = {"objectId": object_id}
        if recure is not None:
            params["recure"] = str(recure).lower()
        if relation_type_id is not None:
            params["relationTypeId"] = relation_type_id
        data = await self._request("get", "/core/api/Relations/EntersInVersion", params=params)
        return [ObjectRelation.model_validate(item) for item in data]
