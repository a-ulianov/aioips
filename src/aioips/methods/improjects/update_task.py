"""Метод обновления задачи проекта (Improject, мутация)."""

from typing import Any

from ...core import APIManager


class UpdateTaskMixin(APIManager):
    """Реализует ``PUT /core/api/improjects/task/{taskId}`` (``ImProject_UpdateTask``)."""

    async def update_task(
        self: "UpdateTaskMixin",
        task_id: int,
        request: dict[str, Any],
        *,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Обновляет существующую задачу проекта Improject (МУТАЦИЯ).

        Назначение: изменить поля задачи (текст, сроки, прогресс, назначения)
        на диаграмме Ганта. Применяйте для редактирования уже созданной
        :meth:`create_task` задачи. Идентификаторы задач берут из проекта,
        загруженного :meth:`project`.

        Предусловие: задача ``task_id`` существует; модуль Improject
        лицензирован. Тело ``request`` соответствует DTO ``TaskSaveDto`` (ключи
        ``camelCase``): ``taskData`` (``TaskDto``), опционально ``attachments``.

        Обратимость: ОБРАТИМА по смыслу — повторным :meth:`update_task` с
        прежними значениями полей. Перед изменением рекомендуется прочитать
        текущее состояние :meth:`task`, чтобы иметь данные для отката.

        Защита: меняет данные на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            task_id: Числовой идентификатор задачи (``taskId`` в пути).
            request: Тело ``TaskSaveDto`` (словарь, ключи ``camelCase``):
                ``taskData`` и опционально ``attachments``.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Словарь результата ``GanttOperationResult``. Значимый ключ
            ``action`` — описание выполненной операции Ганта (``GanttAction``).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если задача не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.update_task(
                    7200,
                    {"taskData": {"id": 7200, "progress": 0.75}},
                    confirm=True,
                )

        Notes:
            ``operationId``: ``ImProject_UpdateTask``; путь
            ``PUT /core/api/improjects/task/{taskId}`` (тело ``TaskSaveDto``,
            ответ ``GanttOperationResult``). Связанные методы: :meth:`create_task`,
            :meth:`delete_task`, :meth:`task`.
        """
        if confirm is not True:
            raise ValueError(
                "update_task изменяет задачу проекта; передайте confirm=True",
            )
        data = await self._request("put", f"/core/api/improjects/task/{task_id}", json=request)
        result: dict[str, Any] = data if isinstance(data, dict) else {}
        return result
