"""Метод получения списка типов связей."""

from ...core import APIManager
from ...schemas.relations import RelationType


class RelationTypesMixin(APIManager):
    """Реализует ``GET /core/api/Relations/GetRelationTypes``.

    operationId: ``Relations_GetRelationTypes``.
    """

    async def relation_types(self: "RelationTypesMixin") -> list[RelationType]:
        """Возвращает список всех типов связей, определённых в IPS.

        Тип связи задаёт семантику направленного отношения родитель → потомок; у него есть
        прямое наименование (``name``, со стороны родителя) и обратное (``reverse_name``,
        со стороны потомка). Идентификаторы типов связей используются в
        :meth:`relations_by_project` и при создании связей.

        Когда применять: чтобы узнать ``id`` нужного типа связи (например, «состав изделия»)
        перед чтением состава через :meth:`relations_by_project` или перечислением связей
        типа через :meth:`relation_type_relations`. Предусловий нет (справочник метаданных).

        Returns:
            Список типов связей по схеме :class:`RelationType`. Пустой список означает, что
            типов связей в базе нет (а также при неожиданной форме ответа сервера —
            не-список приводится к ``[]``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                types = await ips.relation_types()
                by_id = {t.id: t.name for t in types}

        Notes:
            operationId ``Relations_GetRelationTypes``; путь
            ``GET /core/api/Relations/GetRelationTypes`` (массив ``RelationTypeDTO``).
            ``id`` типа связи — отдельное id-пространство ТИПОВ связей (``RelationType``
            в DTO связи), не путать с ``RelationID`` конкретной связи.
        """
        data = await self._request("get", "/core/api/Relations/GetRelationTypes")
        items = data if isinstance(data, list) else []
        return [RelationType.model_validate(item) for item in items]
