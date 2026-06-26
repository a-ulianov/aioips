"""Метод получения назначений ресурсов проектов (Improject)."""

from ...core import APIManager
from ...schemas.improjects import ResourceAssignments


class ResourceAssignmentsMixin(APIManager):
    """Реализует ``GET /core/api/improjects/resourceAssignments``.

    ``operationId`` ``ImProject_GetResourceAssignments``.
    """

    async def resource_assignments(self: "ResourceAssignmentsMixin") -> ResourceAssignments:
        """Возвращает сводку назначений ресурсов на задачи проектов Improject.

        Используйте для оценки занятости ресурсов: метод сводит вместе задачи,
        участвующие ресурсы и пользователей. В отличие от :meth:`project`, не
        привязан к одному проекту и не требует идентификатора — отдаёт назначения по
        доступным проектам. Подробности отдельной задачи получают через :meth:`task`.

        Предусловие: модуль Improject (управление проектами) должен быть лицензирован.

        Returns:
            Назначения по схеме :class:`ResourceAssignments`. ``data`` — задачи
            (``TaskDto``, «сырые»), ``resources`` — ресурсы (``ResourceDto``, «сырые»),
            ``users`` — идентификаторы пользователей. Пустые коллекции означают
            отсутствие назначений.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                assignments = await ips.resource_assignments()
                print(len(assignments.resources), assignments.users)

        Notes:
            ``operationId``: ``ImProject_GetResourceAssignments``; путь
            ``GET /core/api/improjects/resourceAssignments`` (ответ ``ResourceAssignmentsDto``).
        """
        data = await self._request("get", "/core/api/improjects/resourceAssignments")
        return ResourceAssignments.model_validate(data)
