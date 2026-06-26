"""Метод получения настроек графических подписей (штампов ЭЦП) архива."""

from ...core import APIManager
from ...schemas.graph_signs import AssignedSignGraphGroup


class ArchiveSignSettingsMixin(APIManager):
    """Реализует метод ``GET /api/archives/{archiveId}/signs`` (``Sign_GetArchiveSignSettings``)."""

    async def archive_sign_settings(
        self: "ArchiveSignSettingsMixin",
        archive_id: int,
    ) -> list[AssignedSignGraphGroup]:
        """Возвращает настройки графических подписей (штампов ЭЦП), назначенных архиву.

        Архиву можно назначить графы подписания (штампы ЭЦП), которые применяются к
        документам этого архива. Метод отдаёт назначенные подписи, сгруппированные в
        именованные группы (см. :class:`~aioips.schemas.graph_signs.AssignedSignGraphGroup`):
        каждая группа содержит список графов с их описанием и признаком строгой проверки.

        Когда применять: для просмотра/настройки подписей конкретного архива. Аналогичные
        настройки для жизненного цикла дают :meth:`lifecycle_level_sign_settings` (уровень)
        и :meth:`lifecycle_step_sign_settings` (шаг). Справочники графов/рангов подписания —
        раздел ``signs`` (:meth:`~aioips.IPSClient.sign_graphs`,
        :meth:`~aioips.IPSClient.sign_ranks`).

        Args:
            archive_id: Идентификатор архива (``archiveId``), для которого запрашиваются
                настройки подписей.

        Returns:
            Список групп :class:`AssignedSignGraphGroup`; у каждой ``name`` — наименование
            группы, ``graphs`` — назначенные графы подписания. Пустой список означает, что
            архиву не назначено графических подписей.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                groups = await ips.archive_sign_settings(1029)
                for g in groups:
                    print(g.name, [s.sign_id for s in g.graphs])

        Notes:
            operationId ``Sign_GetArchiveSignSettings``; путь
            ``GET /api/archives/{archiveId}/signs`` (НЕ ``/core/api``). Ответ — голый массив
            ``AssignedSignGraphGroupContract``.
        """
        data = await self._request("get", f"/api/archives/{archive_id}/signs")
        return [AssignedSignGraphGroup.model_validate(item) for item in data]
