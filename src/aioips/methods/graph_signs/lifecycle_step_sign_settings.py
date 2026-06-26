"""Метод получения настроек графических подписей (штампов ЭЦП) шага ЖЦ."""

from ...core import APIManager
from ...schemas.graph_signs import AssignedSignGraphGroup


class LifecycleStepSignSettingsMixin(APIManager):
    """Реализует ``GET /api/lifecycleSteps/{lifecycleStepId}/signs``.

    operationId ``Sign_GetLifecycleStepSignSettings``.
    """

    async def lifecycle_step_sign_settings(
        self: "LifecycleStepSignSettingsMixin",
        lifecycle_step_id: int,
    ) -> list[AssignedSignGraphGroup]:
        """Возвращает настройки графических подписей (штампов ЭЦП) шага жизненного цикла.

        Шагу жизненного цикла можно назначить графы подписания (штампы ЭЦП), действующие
        для объектов на этом шаге ЖЦ. Метод отдаёт назначенные подписи, сгруппированные в
        именованные группы (см. :class:`~aioips.schemas.graph_signs.AssignedSignGraphGroup`).

        Когда применять: для просмотра/настройки подписей шага ЖЦ. Настройки уровня ЖЦ —
        :meth:`lifecycle_level_sign_settings`, архива — :meth:`archive_sign_settings`.
        Справочники графов/рангов подписания — раздел ``signs``.

        Args:
            lifecycle_step_id: Идентификатор шага жизненного цикла (``lifecycleStepId``).

        Returns:
            Список групп :class:`AssignedSignGraphGroup` (``name`` — имя группы, ``graphs`` —
            назначенные графы подписания). Пустой список — подписи шагу не назначены.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                groups = await ips.lifecycle_step_sign_settings(42)
                for g in groups:
                    print(g.name, len(g.graphs))

        Notes:
            operationId ``Sign_GetLifecycleStepSignSettings``; путь
            ``GET /api/lifecycleSteps/{lifecycleStepId}/signs`` (НЕ ``/core/api``). Ответ —
            голый массив ``AssignedSignGraphGroupContract``.
        """
        data = await self._request("get", f"/api/lifecycleSteps/{lifecycle_step_id}/signs")
        return [AssignedSignGraphGroup.model_validate(item) for item in data]
