"""Метод получения проекта по идентификатору (Improject)."""

from ...core import APIManager
from ...schemas.improjects import Project


class ProjectMixin(APIManager):
    """Реализует метод ``GET /core/api/improjects/{projectId}`` (``ImProject_GetProject``)."""

    async def project(self: "ProjectMixin", project_id: int) -> Project:
        """Возвращает проект Improject (план-график) с задачами, связями и ресурсами.

        Основной способ загрузить один проект управления проектами целиком по его
        числовому идентификатору. Возвращает задачи проекта (диаграмма Ганта),
        зависимости между задачами и назначенные ресурсы. Для подробностей отдельной
        задачи используйте :meth:`task`, для её вложений — :meth:`task_attachments`,
        а для сводки занятости ресурсов — :meth:`resource_assignments`.

        Предусловие: модуль Improject (управление проектами) должен быть лицензирован.

        Args:
            project_id: Числовой идентификатор проекта Improject.

        Returns:
            Проект по схеме :class:`Project`. Поле ``id`` — идентификатор проекта;
            ``data`` — список задач (``TaskDto``), ``links`` — зависимости,
            ``resources`` — ресурсы, ``display_settings`` — настройки отображения.
            Вложенные структуры возвращаются «сырыми» (``dict``/``list[dict]``).

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если проект не найден).

        Example:
            async with IPSClient(config=config) as ips:
                proj = await ips.project(1500)
                print(proj.id, len(proj.data))

        Notes:
            ``operationId``: ``ImProject_GetProject``; путь
            ``GET /core/api/improjects/{projectId}`` (ответ ``ProjectDto``).
        """
        data = await self._request("get", f"/core/api/improjects/{project_id}")
        return Project.model_validate(data)
