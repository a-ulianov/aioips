"""Метод повышения уровня задачи в иерархии проекта (Improject, мутация)."""

from typing import Any

from ...core import APIManager


class MoveTaskLevelUpMixin(APIManager):
    """Реализует ``POST /core/api/improjects/task/{taskId}/moveLevelUp``.

    ``operationId``: ``ImProject_MoveTaskLevelUp``.
    """

    async def move_task_level_up(
        self: "MoveTaskLevelUpMixin",
        task_id: int,
        *,
        new_parent_task_id: int | None = None,
        new_prev_task_id: int | None = None,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Повышает уровень задачи в иерархии проекта Improject (выносит из подзадач) (МУТАЦИЯ).

        Назначение: сместить задачу на уровень выше в структуре декомпозиции
        (WBS) диаграммы Ганта — задача перестаёт быть дочерней. Применяйте при
        перестроении иерархии этапов. Обратная операция —
        :meth:`move_task_level_down`.

        Предусловие: задача ``task_id`` существует; модуль Improject лицензирован.

        Обратимость: ОБРАТИМА — уровень возвращается :meth:`move_task_level_down`.

        Защита: меняет структуру проекта, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            task_id: Числовой идентификатор перемещаемой задачи (``taskId`` в пути).
            new_parent_task_id: Идентификатор новой родительской задачи
                (query ``newParentTaskId``). ``None`` — не передаётся.
            new_prev_task_id: Идентификатор задачи, после которой разместить
                (query ``newPrevTaskId``). ``None`` — не передаётся.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Словарь результата ``GanttOperationResult`` (значимый ключ
            ``action`` — описание операции Ганта).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.move_task_level_up(7200, confirm=True)

        Notes:
            ``operationId``: ``ImProject_MoveTaskLevelUp``; путь
            ``POST /core/api/improjects/task/{taskId}/moveLevelUp`` (query
            ``newParentTaskId``, ``newPrevTaskId``; тело ``{}`` против 415; ответ
            ``GanttOperationResult``). Обратный метод: :meth:`move_task_level_down`.
        """
        if confirm is not True:
            raise ValueError(
                "move_task_level_up меняет иерархию задач; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if new_parent_task_id is not None:
            params["newParentTaskId"] = new_parent_task_id
        if new_prev_task_id is not None:
            params["newPrevTaskId"] = new_prev_task_id
        data = await self._request(
            "post",
            f"/core/api/improjects/task/{task_id}/moveLevelUp",
            params=params,
            json={},
        )
        result: dict[str, Any] = data if isinstance(data, dict) else {}
        return result
