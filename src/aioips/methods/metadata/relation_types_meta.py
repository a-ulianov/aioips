"""Метод получения списка типов связей метаданных."""

from ...core import APIManager
from ...schemas.metadata import RelationTypeMeta


class RelationTypesMetaMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/relationTypes``."""

    async def relation_types_meta(self: "RelationTypesMetaMixin") -> list[RelationTypeMeta]:
        """Возвращает список всех типов связей, определённых в метаданных IPS.

        Тип связи (``RelationType``) описывает семантику ребра между объектами:
        прямое имя (``type_name``, например «Входит в»), обратное имя
        (``reverse_name``, например «Состоит из») и вид связи (иерархическая /
        неиерархическая). Этот справочник задаёт id-пространство ТИПОВ связей,
        используемое при работе с составом и связями объектов (разделы
        ``relation_types`` и ``relation_queries``).

        Когда применять: чтобы получить весь словарь типов связей разом (например,
        построить отображение ``id → type_name`` или подобрать тип связи для
        добавления потомка в состав). Для точечного запроса по одному id/guid
        дешевле :meth:`relation_type_meta` / :meth:`relation_type_meta_by_guid`.
        Тип связи по умолчанию для родительского типа объекта —
        :meth:`default_relation_type_id`.

        Returns:
            Список типов связей по схеме :class:`RelationTypeMeta`. Пустой список
            означает, что в базе не определено ни одного типа связи.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                types = await ips.relation_types_meta()
                by_name = {t.id: t.type_name for t in types}

        Notes:
            operationId ``Metadata_GetRelationTypeList``; путь
            ``GET /core/api/metadata/relationTypes`` (массив ``ImsRelationTypeDto``).
            Связанные методы: :meth:`relation_type_meta`,
            :meth:`default_relation_type_id`.
        """
        data = await self._request("get", "/core/api/metadata/relationTypes")
        return [RelationTypeMeta.model_validate(item) for item in data]
