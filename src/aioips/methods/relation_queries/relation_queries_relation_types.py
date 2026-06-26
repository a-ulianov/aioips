"""Метод получения справочника типов связей (раздел запросов состава)."""

from ...core import APIManager
from ...schemas.relation_queries import RelationTypeBrief


class RelationQueriesRelationTypesMixin(APIManager):
    """Реализует ``GET /core/api/Relations/GetRelationTypes`` (``Relations_GetRelationTypes``)."""

    async def relation_queries_relation_types(
        self: "RelationQueriesRelationTypesMixin",
    ) -> list[RelationTypeBrief]:
        """Возвращает справочник типов связей, определённых в IPS.

        Тип связи задаёт семантику ребра состава/вхождения; его идентификатор
        используется как фильтр ``relation_type_id`` в :meth:`consist_from` и
        :meth:`enters_in_version`, а также встречается в поле ``relation_type_id``
        возвращаемых записей :class:`~aioips.schemas.relation_queries.ObjectRelation`.
        Метод относится к разделу запросов состава (контроллер
        ``/core/api/Relations/...`` с ЗАГЛАВНОЙ ``R``) и не совпадает с разделом
        ``relations`` (строчная ``r``). Предусловий нет.

        Returns:
            Список типов связей по схеме :class:`RelationTypeBrief`. Поле ``name`` —
            наименование прямого направления, ``reverse_name`` — обратного. Пустой
            список означает, что типы связей в базе не определены.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                types = await ips.relation_queries_relation_types()
                by_id = {t.id: t.name for t in types}

        Notes:
            operationId ``Relations_GetRelationTypes``; путь
            ``GET /core/api/Relations/GetRelationTypes`` (массив ``RelationTypeDTO``).
        """
        data = await self._request("get", "/core/api/Relations/GetRelationTypes")
        return [RelationTypeBrief.model_validate(item) for item in data]
