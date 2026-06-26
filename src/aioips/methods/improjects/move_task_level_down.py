"""Метод понижения уровня задачи в иерархии проекта (Improject, мутация)."""

from typing import Any

from ...core import APIManager


class MoveTaskLevelDownMixin(APIManager):
    """Реализует ``POST /core/api/improjects/task/{taskId}/moveLevelDown``.

    ``operationId``: ``ImProject_MoveTaskLevelDown``.
    """

    async def move_task_level_down(
        self: "MoveTaskLevelDownMixin",
        task_id: int,
        *,
        new_parent_task_id: int | None = None,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Понижает уровень задачи в иерархии проекта Improject (делает подзадачей) (МУТАЦИЯ).

        Назначение: сместить задачу на уровень ниже в структуре декомпозиции
        (WBS) диаграммы Ганта — задача становится дочерней. Применяйте при
        выстраивании иерархии этапов. Обратная операция — :meth:`move_task_level_up`.

        Предусловие: задача ``task_id`` существует; модуль Improject лицензирован.

        Обратимость: ОБРАТИМА — уровень возвращается :meth:`move_task_level_up`.

        Защита: меняет структуру проекта, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            task_id: Числовой идентификатор перемещаемой задачи (``taskId`` в пути).
            new_parent_task_id: Идентификатор новой родительской задачи
                (query ``newParentTaskId``). ``None`` — не передаётся.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Словарь результата ``GanttOperationResult`` (значимый ключ
            ``action`` — описание операции Ганта).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.move_task_level_down(7200, new_parent_task_id=7100, confirm=True)

        Notes:
            ``operationId``: ``ImProject_MoveTaskLevelDown``; путь
            ``POST /core/api/improjects/task/{taskId}/moveLevelDown`` (query
            ``newParentTaskId``; тело ``{}`` против 415; ответ
            ``GanttOperationResult``). Обратный метод: :meth:`move_task_level_up`.
        """
        if confirm is not True:
            raise ValueError(
                "move_task_level_down меняет иерархию задач; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if new_parent_task_id is not None:
            params["newParentTaskId"] = new_parent_task_id
        data = await self._request(
            "post",
            f"/core/api/improjects/task/{task_id}/moveLevelDown",
            params=params,
            json={},
        )
        result: dict[str, Any] = data if isinstance(data, dict) else {}
        return result
