"""Метод записи настроек графических подписей (штампов ЭЦП) архива (мутация)."""

from typing import Any

from ...core import APIManager
from ...schemas.graph_signs import AssignedSignGraphGroup


class UpdateArchiveSignSettingsMixin(APIManager):
    """Реализует ``POST /api/archives/{archiveId}/signs``.

    operationId ``Sign_UpdateArchiveSignSettings``.
    """

    async def update_archive_sign_settings(
        self: "UpdateArchiveSignSettingsMixin",
        archive_id: int,
        groups: list[AssignedSignGraphGroup] | list[dict[str, Any]],
        *,
        confirm: bool = False,
    ) -> None:
        """Записывает настройки графических подписей (штампов ЭЦП) архива (МУТАЦИЯ, ``confirm``).

        Полностью переопределяет набор групп графов подписания, назначенных архиву: какие
        штампы ЭЦП применяются к документам этого архива. Это **config-настройка подписей**
        (визуальные штампы / графы подписания документов), а НЕ права доступа к архиву — на
        состав/права она не влияет. Парная запись к read-методу :meth:`archive_sign_settings`.

        Когда применять: чтобы задать/изменить графы подписания архива. Тело заменяет
        настройки целиком (это перезапись, не слияние): передавайте полный итоговый список
        групп. Аналоги: уровень ЖЦ — :meth:`update_lifecycle_level_sign_settings`, шаг ЖЦ —
        :meth:`update_lifecycle_step_sign_settings`.

        Обратимость: операция обратима. Перед записью прочитайте текущие настройки парным
        :meth:`archive_sign_settings` и сохраните их; при откате запишите этот снимок обратно
        этим же методом (write-same-back). Для проверки в тесте: прочитать → записать тот же
        список обратно — состояние не меняется.

        Защита: мутация защищена ``confirm`` — без ``confirm=True`` поднимается
        :class:`ValueError` ещё ДО обращения к серверу (запрос не выполняется).

        Args:
            archive_id: Идентификатор архива (``archiveId``; id-пространство архивов —
                объект архива, не версия документа). Передаётся в пути.
            groups: Полный список групп графов подписания
                (:class:`AssignedSignGraphGroup`) или эквивалентных словарей
                (``AssignedSignGraphGroupContract``). Для точного round-trip без потери
                полей передавайте «сырой» список из ответа :meth:`archive_sign_settings`.
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                current = await ips.archive_sign_settings(1029)        # бэкап
                await ips.update_archive_sign_settings(
                    1029, current, confirm=True
                )                                                       # запись обратно

        Notes:
            operationId ``Sign_UpdateArchiveSignSettings``; путь
            ``POST /api/archives/{archiveId}/signs`` (НЕ ``/core/api``); тело — массив
            ``AssignedSignGraphGroupContract``. Парный read — :meth:`archive_sign_settings`.
        """
        if confirm is not True:
            raise ValueError(
                "update_archive_sign_settings мутирует настройки подписей; передайте confirm=True"
            )
        if groups and isinstance(groups[0], AssignedSignGraphGroup):
            payload: list[dict[str, Any]] = [
                g.model_dump(mode="json", by_alias=True, exclude_none=True)
                for g in groups
                if isinstance(g, AssignedSignGraphGroup)
            ]
        else:
            payload = [g for g in groups if isinstance(g, dict)]
        await self._request("post", f"/api/archives/{archive_id}/signs", json=payload)
        return None
