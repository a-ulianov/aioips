"""Метод получения типа связи для связи проекта (prjLink)."""

from ...core import APIManager


class RelationTypeForPrjLinkMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/relationTypeForPrjLink/{prjLinkId}``."""

    async def relation_type_for_prj_link(
        self: "RelationTypeForPrjLinkMixin",
        prj_link_id: int,
    ) -> int:
        """Возвращает id типа связи для заданной связи проекта (prjLink).

        Сопоставляет конкретную проектную связь (``prjLink``) с её типом связи
        (``RelationType``) в метаданных. Удобно, когда есть идентификатор связи проекта,
        но нужны метаданные её типа (для последующих запросов по ``relationTypeId``).
        Ответ сервера — целое число (идентификатор типа связи), а не объект-обёртка.

        Когда применять: как мост «prjLink → relationType» перед обращением к
        метаданным типа связи (:meth:`relation_type_meta` и др.).

        Args:
            prj_link_id: Идентификатор связи проекта (``prjLinkId``; id-пространство
                проектных связей, не тип связи и не объект).

        Returns:
            Числовой идентификатор типа связи (``RelationType``; id-пространство ТИПОВ
            связей). Сервер не возвращает ``None``: при отсутствии связи — ошибка.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если связь проекта с
                таким id не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                relation_type_id = await ips.relation_type_for_prj_link(12345)

        Notes:
            operationId ``Metadata_GetRelationTypeForPrjLinkId``; путь
            ``GET /core/api/metadata/relationTypeForPrjLink/{prjLinkId}`` (ответ —
            ``int``). Связанные методы: :meth:`relation_type_meta`.
        """
        path = f"/core/api/metadata/relationTypeForPrjLink/{prj_link_id}"
        data = await self._request("get", path)
        return int(data)
