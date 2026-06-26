"""Метод получения настроек графических подписей (штампов ЭЦП) для ранга."""

from ...core import APIManager
from ...schemas.graph_signs import RankGraphSigns


class RankGraphSignsMixin(APIManager):
    """Реализует ``GET /api/ranks/{rankId}/graphSigns`` (``RankGraphSign_GetRankGraphSigns``)."""

    async def rank_graph_signs(
        self: "RankGraphSignsMixin",
        rank_id: int,
    ) -> list[RankGraphSigns]:
        """Возвращает настройки графических подписей ранга, сгруппированные по типу объекта.

        Графическая подпись (штамп ЭЦП) ранга определяет, какие графы подписания и с
        какими правилами (простая/криптографическая подпись, запрет множественного
        подписания) применяются к объектам каждого типа в рамках данного ранга. Метод
        отдаёт уже заданные настройки ранга — по одной записи на тип объекта.

        Когда применять: для просмотра/редактирования настроек подписей конкретного ранга.
        Перечень типов объектов, которые ещё можно добавить, отдаёт
        :meth:`rank_graph_sign_object_types`. Справочник графов подписания —
        :meth:`~aioips.IPSClient.sign_graphs`, рангов подписания —
        :meth:`~aioips.IPSClient.sign_ranks` (раздел ``signs``).

        Args:
            rank_id: Идентификатор ранга (``rankId``), для которого запрашиваются настройки
                графических подписей.

        Returns:
            Список :class:`RankGraphSigns`; у каждого элемента ``object_type_id`` — тип
            объекта, ``graphs`` — настройки графов подписания (см.
            :class:`~aioips.schemas.graph_signs.RankGraphSignsSettings`). Пустой список
            означает, что для ранга не задано ни одной настройки.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                settings = await ips.rank_graph_signs(10)
                for s in settings:
                    print(s.object_type_id, len(s.graphs))

        Notes:
            operationId ``RankGraphSign_GetRankGraphSigns``; путь
            ``GET /api/ranks/{rankId}/graphSigns`` (НЕ ``/core/api``). Ответ — голый массив
            ``RankGraphSignsContract``.
        """
        data = await self._request("get", f"/api/ranks/{rank_id}/graphSigns")
        return [RankGraphSigns.model_validate(item) for item in data]
