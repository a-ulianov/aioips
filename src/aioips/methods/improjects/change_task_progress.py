"""Метод изменения прогресса задачи проекта (Improject, мутация)."""

from typing import Any

from ...core import APIManager


class ChangeTaskProgressMixin(APIManager):
    """Реализует ``POST /core/api/improjects/tasks/{taskId}/changeProgress``.

    ``operationId``: ``ImProject_ChangeTaskProgress``.
    """

    async def change_task_progress(
        self: "ChangeTaskProgressMixin",
        task_id: int,
        *,
        progress: float | None = None,
        is_need_to_log_modification_history: bool | None = None,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Изменяет процент выполнения (прогресс) задачи проекта Improject (МУТАЦИЯ).

        Назначение: обновить готовность задачи на диаграмме Ганта (доля
        выполнения). Применяйте при отметке хода работ. Прогресс задаётся
        долей в диапазоне ``0..1`` (query ``progress``). Полное обновление
        прочих полей задачи — через :meth:`update_task`.

        Предусловие: задача ``task_id`` существует; модуль Improject лицензирован.

        Обратимость: ОБРАТИМА — повторным :meth:`change_task_progress` с прежним
        значением ``progress``.

        Защита: меняет данные на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            task_id: Числовой идентификатор задачи (``taskId`` в пути).
            progress: Доля выполнения ``0..1`` (query ``progress``). ``None`` —
                не передаётся.
            is_need_to_log_modification_history: Логировать ли изменение в
                историю (query ``isNeedToLogModificationHistory``). ``None`` —
                не передаётся.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Словарь карточки задачи ``TaskInfoDto`` (распакован из обёртки
            ``TaskInfoDtoProcessResultWithLogInfoDto`` по ключу ``result``).
            Значимые ключи: ``projectId``, ``taskData`` (``TaskDto``).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                info = await ips.change_task_progress(7200, progress=0.5, confirm=True)
                print(info["taskData"]["progress"])

        Notes:
            ``operationId``: ``ImProject_ChangeTaskProgress``; путь
            ``POST /core/api/improjects/tasks/{taskId}/changeProgress`` (query
            ``progress``, ``isNeedToLogModificationHistory``; тело ``{}`` против
            415; ответ ``TaskInfoDtoProcessResultWithLogInfoDto``).
        """
        if confirm is not True:
            raise ValueError(
                "change_task_progress меняет прогресс задачи; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if progress is not None:
            params["progress"] = str(progress)
        if is_need_to_log_modification_history is not None:
            params["isNeedToLogModificationHistory"] = str(
                is_need_to_log_modification_history
            ).lower()
        data = await self._request(
            "post",
            f"/core/api/improjects/tasks/{task_id}/changeProgress",
            params=params,
            json={},
        )
        if isinstance(data, dict):
            result: dict[str, Any] = data.get("result", data) or {}
            return result
        return {}
