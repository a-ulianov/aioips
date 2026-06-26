"""Метод получения вложений задачи проекта (Improject)."""

from ...core import APIManager
from ...schemas.improjects import Attachment


class TaskAttachmentsMixin(APIManager):
    """Реализует ``GET /core/api/improjects/tasks/{taskId}/attachments``.

    ``operationId`` ``ImProject_GetTaskAttachments``.
    """

    async def task_attachments(self: "TaskAttachmentsMixin", task_id: int) -> list[Attachment]:
        """Возвращает список вложений задачи проекта Improject.

        Используйте, чтобы перечислить объекты, прикреплённые к задаче (исходные
        данные и результаты). Каждое вложение ссылается на объект IPS по ``object_id``,
        который можно загрузить целиком через :meth:`object_get`. Сведения о самой
        задаче получают через :meth:`task`.

        Предусловие: модуль Improject (управление проектами) должен быть лицензирован.

        Args:
            task_id: Числовой идентификатор задачи проекта, чьи вложения нужны.

        Returns:
            Список вложений по схеме :class:`Attachment`. Пустой список означает, что
            у задачи нет вложений. У каждого элемента ``object_id`` — идентификатор
            объекта (``objectID``) для :meth:`object_get`, ``caption`` — отображаемое имя.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если задача не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                attachments = await ips.task_attachments(7200)
                for att in attachments:
                    print(att.caption, att.object_id)

        Notes:
            ``operationId``: ``ImProject_GetTaskAttachments``; путь
            ``GET /core/api/improjects/tasks/{taskId}/attachments`` (массив ``AttachmentDto``).
        """
        data = await self._request("get", f"/core/api/improjects/tasks/{task_id}/attachments")
        return [Attachment.model_validate(item) for item in data]
