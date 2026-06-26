"""Метод записи настроек графических подписей (штампов ЭЦП) шага ЖЦ (мутация)."""

from typing import Any

from ...core import APIManager
from ...schemas.graph_signs import AssignedSignGraphGroup


class UpdateLifecycleStepSignSettingsMixin(APIManager):
    """Реализует ``POST /api/lifecycleSteps/{lifecycleStepId}/signs``.

    operationId ``Sign_UpdateLifecycleStepSignSettings``.
    """

    async def update_lifecycle_step_sign_settings(
        self: "UpdateLifecycleStepSignSettingsMixin",
        lifecycle_step_id: int,
        groups: list[AssignedSignGraphGroup] | list[dict[str, Any]],
        *,
        confirm: bool = False,
    ) -> None:
        """Записывает настройки графических подписей шага ЖЦ (МУТАЦИЯ, ``confirm``).

        Полностью переопределяет набор групп графов подписания, назначенных шагу
        жизненного цикла: какие штампы ЭЦП действуют для объектов на этом шаге ЖЦ. Это
        **config-настройка подписей** (визуальные штампы / графы подписания), а НЕ права
        доступа. Парная запись к read-методу :meth:`lifecycle_step_sign_settings`.

        Когда применять: чтобы задать/изменить графы подписания шага ЖЦ. Тело заменяет
        настройки целиком (перезапись, не слияние): передавайте полный итоговый список
        групп. Аналоги: уровень ЖЦ — :meth:`update_lifecycle_level_sign_settings`, архив —
        :meth:`update_archive_sign_settings`.

        Обратимость: операция обратима. Перед записью прочитайте текущие настройки парным
        :meth:`lifecycle_step_sign_settings` и сохраните их; при откате запишите снимок
        обратно этим же методом (write-same-back). Тест: прочитать → записать тот же список
        обратно — состояние не меняется.

        Защита: мутация защищена ``confirm`` — без ``confirm=True`` поднимается
        :class:`ValueError` ещё ДО обращения к серверу (запрос не выполняется).

        Args:
            lifecycle_step_id: Идентификатор шага жизненного цикла (``lifecycleStepId``;
                id-пространство шагов ЖЦ). Передаётся в пути.
            groups: Полный список групп графов подписания
                (:class:`AssignedSignGraphGroup`) или эквивалентных словарей
                (``AssignedSignGraphGroupContract``). Для точного round-trip передавайте
                «сырой» список из ответа :meth:`lifecycle_step_sign_settings`.
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                current = await ips.lifecycle_step_sign_settings(42)   # бэкап
                await ips.update_lifecycle_step_sign_settings(
                    42, current, confirm=True
                )                                                       # запись обратно

        Notes:
            operationId ``Sign_UpdateLifecycleStepSignSettings``; путь
            ``POST /api/lifecycleSteps/{lifecycleStepId}/signs`` (НЕ ``/core/api``); тело —
            массив ``AssignedSignGraphGroupContract``. Парный read —
            :meth:`lifecycle_step_sign_settings`.
        """
        if confirm is not True:
            raise ValueError(
                "update_lifecycle_step_sign_settings мутирует настройки подписей; "
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
        path = f"/api/lifecycleSteps/{lifecycle_step_id}/signs"
        await self._request("post", path, json=payload)
        return None
