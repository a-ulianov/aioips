"""Метод создания задачи в проекте управления проектами (Improject, мутация)."""

from typing import Any

from ...core import APIManager


class CreateTaskMixin(APIManager):
    """Реализует ``POST /core/api/improjects/{projectId}/task`` (``ImProject_CreateTask``)."""

    async def create_task(
        self: "CreateTaskMixin",
        project_id: int,
        request: dict[str, Any],
        *,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Создаёт новую задачу в проекте Improject (строку диаграммы Ганта) (МУТАЦИЯ).

        Назначение: добавить задачу (этап/работу) в существующий проект
        управления проектами. Применяйте после :meth:`create_project` при
        наполнении план-графика. Зависимости между задачами задаются отдельно —
        :meth:`create_dependency`.

        Предусловие: проект ``project_id`` существует; модуль Improject
        лицензирован. Тело ``request`` соответствует DTO ``TaskSaveDto`` (ключи
        ``camelCase``): ``taskData`` — данные задачи (``TaskDto``: ``text``,
        сроки, ``progress``, ``parent`` и т. п.), ``attachments`` — вложения
        (опционально).

        Обратимость: ОБРАТИМА — созданная задача удаляется парным
        :meth:`delete_task` по идентификатору задачи из результата.

        Защита: создаёт задачу на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            project_id: Числовой идентификатор проекта (``projectId`` в пути),
                в который добавляется задача.
            request: Тело ``TaskSaveDto`` (словарь, ключи ``camelCase``):
                ``taskData`` (``TaskDto``) и опционально ``attachments``.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Словарь результата ``CreateTaskResult``. Значимые ключи: ``tid`` —
            идентификатор созданной задачи (для :meth:`delete_task`),
            ``action`` — описание операции Ганта (``GanttAction``).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если проект не найден).

        Example:
            async with IPSClient(config=config) as ips:
                res = await ips.create_task(
                    1500,
                    {"taskData": {"text": "Анализ ТЗ", "progress": 0}},
                    confirm=True,
                )
                task_id = res["tid"]

        Notes:
            ``operationId``: ``ImProject_CreateTask``; путь
            ``POST /core/api/improjects/{projectId}/task`` (тело ``TaskSaveDto``,
            ответ ``CreateTaskResult``). Связанные методы: :meth:`delete_task`,
            :meth:`update_task`, :meth:`create_dependency`.
        """
        if confirm is not True:
            raise ValueError(
                "create_task создаёт задачу в проекте; передайте confirm=True",
            )
        data = await self._request("post", f"/core/api/improjects/{project_id}/task", json=request)
        result: dict[str, Any] = data if isinstance(data, dict) else {}
        return result
