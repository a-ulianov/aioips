"""Метод записи настроек графических подписей шага ЖЦ для типа объекта (мутация)."""

from typing import Any

from ...core import APIManager
from ...schemas.graph_signs import AssignedSignGraphGroup


class UpdateObjectTypeLifecycleStepSignSettingsMixin(APIManager):
    """Реализует ``POST /api/objectTypes/{objectTypeId}/lifecycleSteps/{lifecycleLevelId}/signs``.

    operationId ``Sign_UpdateObjectTypeLifecycleStepSignSettings``.
    """

    async def update_object_type_lifecycle_step_sign_settings(
        self: "UpdateObjectTypeLifecycleStepSignSettingsMixin",
        object_type_id: int,
        lifecycle_level_id: int,
        groups: list[AssignedSignGraphGroup] | list[dict[str, Any]],
        *,
        confirm: bool = False,
    ) -> None:
        """Записывает настройки графических подписей шага ЖЦ для ТИПА объекта (МУТАЦИЯ).

        Полностью переопределяет набор групп графов подписания в узком контексте «тип
        объекта × шаг ЖЦ»: какие штампы ЭЦП назначены объектам данного типа на данном шаге
        ЖЦ. Это **config-настройка подписей** (визуальные штампы / графы подписания), а НЕ
        права доступа. Более узкий контекст, чем
        :meth:`update_lifecycle_step_sign_settings` (шаг безотносительно типа). Парная запись
        к read-методу :meth:`object_type_lifecycle_step_sign_settings`.

        Когда применять: чтобы задать/изменить графы подписания для объектов конкретного
        типа на конкретном шаге ЖЦ. Тело заменяет настройки целиком (перезапись, не
        слияние): передавайте полный итоговый список групп.

        Обратимость: операция обратима. Перед записью прочитайте текущие настройки парным
        :meth:`object_type_lifecycle_step_sign_settings` и сохраните их; при откате запишите
        снимок обратно этим же методом (write-same-back). Тест: прочитать → записать тот же
        список обратно — состояние не меняется.

        Защита: мутация защищена ``confirm`` — без ``confirm=True`` поднимается
        :class:`ValueError` ещё ДО обращения к серверу (запрос не выполняется).

        Args:
            object_type_id: Идентификатор ТИПА объекта (``ObjectTypeID`` — id-пространство
                ТИПОВ, не объекта/версии). Путь ``{objectTypeId}``.
            lifecycle_level_id: Идентификатор шага/уровня ЖЦ (в пути параметр назван
                ``lifecycleLevelId``). Путь ``{lifecycleLevelId}``.
            groups: Полный список групп графов подписания
                (:class:`AssignedSignGraphGroup`) или эквивалентных словарей
                (``AssignedSignGraphGroupContract``). Для точного round-trip передавайте
                «сырой» список из ответа :meth:`object_type_lifecycle_step_sign_settings`.
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                current = await ips.object_type_lifecycle_step_sign_settings(1742, 5)  # бэкап
                await ips.update_object_type_lifecycle_step_sign_settings(
                    1742, 5, current, confirm=True
                )                                                                      # назад

        Notes:
            operationId ``Sign_UpdateObjectTypeLifecycleStepSignSettings``; путь
            ``POST /api/objectTypes/{objectTypeId}/lifecycleSteps/{lifecycleLevelId}/signs``
            (НЕ ``/core/api``); тело — массив ``AssignedSignGraphGroupContract``. Парный
            read — :meth:`object_type_lifecycle_step_sign_settings`.
        """
        if confirm is not True:
            raise ValueError(
                "update_object_type_lifecycle_step_sign_settings мутирует настройки подписей; "
                "передайте confirm=True"
            )
        if groups and isinstance(groups[0], AssignedSignGraphGroup):
            payload: list[dict[str, Any]] = [
                g.model_dump(mode="json", by_alias=True, exclude_none=True)
                for g in groups
                if isinstance(g, AssignedSignGraphGroup)
            ]
        else:
            payload = [g for g in groups if isinstance(g, dict)]
        path = f"/api/objectTypes/{object_type_id}/lifecycleSteps/{lifecycle_level_id}/signs"
        await self._request("post", path, json=payload)
        return None
