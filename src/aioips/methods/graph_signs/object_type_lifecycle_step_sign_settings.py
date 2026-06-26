"""Метод получения настроек графических подписей шага ЖЦ типа объекта."""

from ...core import APIManager
from ...schemas.graph_signs import AssignedSignGraphGroup


class ObjectTypeLifecycleStepSignSettingsMixin(APIManager):
    """Реализует ``GET /api/objectTypes/{objectTypeId}/lifecycleSteps/{lifecycleLevelId}/signs``.

    operationId ``Sign_GetObjectTypeLifecycleStepSignSettings``.
    """

    async def object_type_lifecycle_step_sign_settings(
        self: "ObjectTypeLifecycleStepSignSettingsMixin",
        object_type_id: int,
        lifecycle_level_id: int,
    ) -> list[AssignedSignGraphGroup]:
        """Возвращает настройки графических подписей шага ЖЦ для конкретного ТИПА объекта.

        Уточняет настройки подписей (штампов ЭЦП) шага жизненного цикла применительно к
        конкретному типу объекта: какие графы подписания назначены объектам данного типа
        на данном шаге ЖЦ. Это более узкий контекст, чем :meth:`lifecycle_step_sign_settings`
        (настройки шага безотносительно типа): здесь связка «тип объекта × шаг ЖЦ».

        Когда применять: для просмотра подписей, действующих для объектов конкретного типа
        на конкретном шаге ЖЦ. Только чтение. Настройки уровня ЖЦ —
        :meth:`lifecycle_level_sign_settings`, архива — :meth:`archive_sign_settings`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (``ObjectTypeID`` — id-пространство
                ТИПОВ, не объекта/версии). Путь ``{objectTypeId}``.
            lifecycle_level_id: Идентификатор шага/уровня ЖЦ (в пути параметр назван
                ``lifecycleLevelId``). Путь ``{lifecycleLevelId}``.

        Returns:
            Список групп :class:`AssignedSignGraphGroup` (``name`` — имя группы, ``graphs`` —
            назначенные графы подписания). Пустой список — подписи не назначены.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                groups = await ips.object_type_lifecycle_step_sign_settings(1742, 5)
                for g in groups:
                    print(g.name, len(g.graphs))

        Notes:
            operationId ``Sign_GetObjectTypeLifecycleStepSignSettings``; путь
            ``GET /api/objectTypes/{objectTypeId}/lifecycleSteps/{lifecycleLevelId}/signs``
            (НЕ ``/core/api``). Ответ — голый массив ``AssignedSignGraphGroupContract``.
            Связанные: :meth:`lifecycle_step_sign_settings`, :meth:`archive_sign_settings`.
        """
        path = f"/api/objectTypes/{object_type_id}/lifecycleSteps/{lifecycle_level_id}/signs"
        data = await self._request("get", path)
        if not isinstance(data, list):
            return []
        return [AssignedSignGraphGroup.model_validate(item) for item in data]
