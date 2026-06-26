"""Метод получения настроек графических подписей (штампов ЭЦП) уровня ЖЦ."""

from ...core import APIManager
from ...schemas.graph_signs import AssignedSignGraphGroup


class LifecycleLevelSignSettingsMixin(APIManager):
    """Реализует ``GET /api/lifecycleLevels/{lifecycleLevelId}/signs``.

    operationId ``Sign_GetLifecycleLevelSignSettings``.
    """

    async def lifecycle_level_sign_settings(
        self: "LifecycleLevelSignSettingsMixin",
        lifecycle_level_id: int,
    ) -> list[AssignedSignGraphGroup]:
        """Возвращает настройки графических подписей (штампов ЭЦП) уровня жизненного цикла.

        Уровню жизненного цикла можно назначить графы подписания (штампы ЭЦП), действующие
        для объектов на этом уровне ЖЦ. Метод отдаёт назначенные подписи, сгруппированные в
        именованные группы (см. :class:`~aioips.schemas.graph_signs.AssignedSignGraphGroup`).

        Когда применять: для просмотра/настройки подписей уровня ЖЦ. Настройки шага ЖЦ —
        :meth:`lifecycle_step_sign_settings`, архива — :meth:`archive_sign_settings`.
        Справочники графов/рангов подписания — раздел ``signs``.

        Args:
            lifecycle_level_id: Идентификатор уровня жизненного цикла (``lifecycleLevelId``).

        Returns:
            Список групп :class:`AssignedSignGraphGroup` (``name`` — имя группы, ``graphs`` —
            назначенные графы подписания). Пустой список — подписи уровню не назначены.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                groups = await ips.lifecycle_level_sign_settings(3)
                for g in groups:
                    print(g.name, len(g.graphs))

        Notes:
            operationId ``Sign_GetLifecycleLevelSignSettings``; путь
            ``GET /api/lifecycleLevels/{lifecycleLevelId}/signs`` (НЕ ``/core/api``). Ответ —
            голый массив ``AssignedSignGraphGroupContract``.
        """
        data = await self._request("get", f"/api/lifecycleLevels/{lifecycle_level_id}/signs")
        return [AssignedSignGraphGroup.model_validate(item) for item in data]
