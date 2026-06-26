"""Метод изменения порядка задачи в проекте (Improject, мутация)."""

from typing import Any

from ...core import APIManager


class ReorderTaskMixin(APIManager):
    """Реализует ``POST /core/api/improjects/task/{taskId}/reorder``.

    ``operationId``: ``ImProject_ReorderTask``.
    """

    async def reorder_task(
        self: "ReorderTaskMixin",
        task_id: int,
        *,
        new_parent_task_id: int | None = None,
        new_prev_task_id: int | None = None,
        new_next_task_id: int | None = None,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Меняет порядок (позицию) задачи в проекте Improject (МУТАЦИЯ).

        Назначение: переместить задачу в другую позицию списка/иерархии задач
        диаграммы Ганта — задать нового родителя и/или соседей (до/после).
        Применяйте при ручной сортировке задач. В отличие от
        :meth:`move_task_level_up`/:meth:`move_task_level_down` (смена уровня),
        этот метод управляет именно порядком внутри уровня.

        Предусловие: задача ``task_id`` существует; модуль Improject лицензирован.

        Обратимость: ОБРАТИМА — повторным :meth:`reorder_task` с прежними
        соседями восстанавливается исходный порядок.

        Защита: меняет структуру проекта, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            task_id: Числовой идентификатор перемещаемой задачи (``taskId`` в пути).
            new_parent_task_id: Новый родитель (query ``newParentTaskId``).
                ``None`` — не передаётся.
            new_prev_task_id: Предыдущая соседняя задача (query ``newPrevTaskId``).
                ``None`` — не передаётся.
            new_next_task_id: Следующая соседняя задача (query ``newNextTaskId``).
                ``None`` — не передаётся.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Словарь результата ``GanttOperationResult`` (значимый ключ
            ``action`` — описание операции Ганта).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.reorder_task(7200, new_prev_task_id=7100, confirm=True)

        Notes:
            ``operationId``: ``ImProject_ReorderTask``; путь
            ``POST /core/api/improjects/task/{taskId}/reorder`` (query
            ``newParentTaskId``, ``newPrevTaskId``, ``newNextTaskId``; тело ``{}``
            против 415; ответ ``GanttOperationResult``).
        """
        if confirm is not True:
            raise ValueError(
                "reorder_task меняет порядок задач; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if new_parent_task_id is not None:
            params["newParentTaskId"] = new_parent_task_id
        if new_prev_task_id is not None:
            params["newPrevTaskId"] = new_prev_task_id
        if new_next_task_id is not None:
            params["newNextTaskId"] = new_next_task_id
        data = await self._request(
            "post",
            f"/core/api/improjects/task/{task_id}/reorder",
            params=params,
            json={},
        )
        result: dict[str, Any] = data if isinstance(data, dict) else {}
        return result
