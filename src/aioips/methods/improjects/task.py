"""Метод получения сведений о задаче проекта (Improject)."""

from ...core import APIManager
from ...schemas.improjects import Task


class TaskMixin(APIManager):
    """Реализует метод ``GET /core/api/improjects/tasks/{taskId}`` (``ImProject_GetTask``)."""

    async def task(self: "TaskMixin", task_id: int) -> Task:
        """Возвращает сведения об одной задаче проекта Improject (карточку задачи).

        Используйте, когда нужны подробности конкретной задачи (контекст проекта,
        данные задачи, ответ руководителя), а не весь проект целиком. Идентификаторы
        задач можно получить из задач проекта, загруженного :meth:`project`
        (поле ``data``). Вложения задачи получают отдельно — :meth:`task_attachments`.

        Предусловие: модуль Improject (управление проектами) должен быть лицензирован.

        Args:
            task_id: Числовой идентификатор задачи проекта.

        Returns:
            Задача по схеме :class:`Task`. ``task_data`` — «сырые» данные задачи
            (``TaskDto``); ``project_id``/``project_name`` — контекст проекта;
            ``manager_answer`` — резолюция руководителя (``None``, если отсутствует).

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если задача не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                t = await ips.task(7200)
                print(t.project_name, t.task_data.get("text"))

        Notes:
            ``operationId``: ``ImProject_GetTask``; путь
            ``GET /core/api/improjects/tasks/{taskId}`` (ответ ``TaskInfoDto``).
        """
        data = await self._request("get", f"/core/api/improjects/tasks/{task_id}")
        return Task.model_validate(data)
