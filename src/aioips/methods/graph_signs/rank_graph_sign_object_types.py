"""Метод получения типов объектов, доступных для настроек графических подписей ранга."""

from ...core import APIManager


class RankGraphSignObjectTypesMixin(APIManager):
    """Реализует метод ``GET /api/ranks/graphSigns/availableObjectTypeIds``.

    operationId ``RankGraphSign_GetObjectTypeIdsAvailableForAddingToEditingContext``.
    """

    async def rank_graph_sign_object_types(self: "RankGraphSignObjectTypesMixin") -> list[int]:
        """Возвращает id типов объектов, доступных для добавления в настройки подписей ранга.

        Графические подписи (штампы ЭЦП) ранга задаются по типам объектов: для каждого
        типа объекта определяется набор графов подписания. Метод отдаёт идентификаторы
        тех типов объектов, которые ещё можно добавить в контекст редактирования настроек
        подписей ранга (то есть допустимые кандидаты для новой группы настроек).

        Когда применять: при построении UI настройки графических подписей ранга — чтобы
        предложить выбор типа объекта, для которого добавляются настройки. Уже заданные
        настройки ранга (по типам объектов) отдаёт :meth:`rank_graph_signs`. Справочник
        самих графов подписания — :meth:`~aioips.IPSClient.sign_graphs` (раздел ``signs``).
        Предусловий нет; это справочный read-метод.

        Returns:
            Список числовых идентификаторов типов объектов. Пустой список означает, что
            нет типов объектов, доступных для добавления.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                type_ids = await ips.rank_graph_sign_object_types()
                print(type_ids)

        Notes:
            operationId ``RankGraphSign_GetObjectTypeIdsAvailableForAddingToEditingContext``;
            путь ``GET /api/ranks/graphSigns/availableObjectTypeIds`` (НЕ ``/core/api``).
            Ответ — голый массив целых.
        """
        data = await self._request("get", "/api/ranks/graphSigns/availableObjectTypeIds")
        return [int(item) for item in data]
