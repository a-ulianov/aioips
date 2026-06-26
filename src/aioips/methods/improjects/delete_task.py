"""Метод удаления задачи проекта (Improject, мутация)."""

from typing import Any

from ...core import APIManager


class DeleteTaskMixin(APIManager):
    """Реализует ``DELETE /core/api/improjects/task/{taskId}`` (``ImProject_DeleteTask``)."""

    async def delete_task(
        self: "DeleteTaskMixin",
        task_id: int,
        *,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Удаляет задачу из проекта Improject (МУТАЦИЯ, необратимо в API).

        Назначение: убрать задачу с диаграммы Ганта. Парная операция к
        :meth:`create_task`. Применяйте при чистке план-графика. Идентификатор
        задачи берут из результата :meth:`create_task` (``tid``) или из проекта
        :meth:`project`.

        Предусловие: задача ``task_id`` существует; модуль Improject
        лицензирован. Удаление задачи может затронуть связанные с ней
        зависимости и подзадачи.

        Обратимость: операция РАЗРУШАЮЩАЯ — отдельного отката нет; восстановление
        возможно только повторным :meth:`create_task` (новый идентификатор).

        Защита: удаляет данные на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            task_id: Числовой идентификатор удаляемой задачи (``taskId`` в пути).
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Словарь результата ``GanttOperationResult``. Значимый ключ
            ``action`` — описание выполненной операции Ганта (``GanttAction``).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если задача не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.delete_task(7200, confirm=True)

        Notes:
            ``operationId``: ``ImProject_DeleteTask``; путь
            ``DELETE /core/api/improjects/task/{taskId}`` (ответ
            ``GanttOperationResult``). Парный метод: :meth:`create_task`.
        """
        if confirm is not True:
            raise ValueError(
                "delete_task удаляет задачу проекта; передайте confirm=True",
            )
        data = await self._request("delete", f"/core/api/improjects/task/{task_id}")
        result: dict[str, Any] = data if isinstance(data, dict) else {}
        return result
