"""Метод получения вложений активности процесса."""

from ...core import APIManager
from ...schemas.workflow import AttachmentsList


class WFAttachmentsMixin(APIManager):
    """Реализует ``GET /core/api/wfAttachments/{activityId}/getAttachmments``.

    operationId ``WFAttachments_GetAttachmments``.
    """

    async def wf_attachments(
        self: "WFAttachmentsMixin",
        activity_id: int,
    ) -> AttachmentsList:
        """Возвращает список объектов, прикреплённых к активности процесса как вложения.

        Вложения активности (задачи) workflow — это объекты IPS, привязанные к шагу
        маршрута. Метод отдаёт видимые текущему пользователю вложения и флаг наличия
        скрытых элементов. Применяйте, чтобы показать или обработать прикреплённые к
        задаче документы; перечень допустимых типов вложений даёт
        :meth:`wf_attachment_allowed_types`, переменные той же активности —
        :meth:`wf_variables`.

        Предусловие по id-пространству: ``activity_id`` — это идентификатор АКТИВНОСТИ
        (задачи) экземпляра процесса, а не идентификатор объекта или версии. Каждый
        элемент результата несёт ``object_id`` (идентификатор ОБЪЕКТА-вложения), по
        которому объект загружается через :meth:`object_get`.

        Args:
            activity_id: Идентификатор активности (задачи) экземпляра процесса workflow.

        Returns:
            :class:`AttachmentsList`: поле ``attachments`` — список вложений
            (:class:`Attachment`), ``has_invisible_items`` — признак того, что часть
            вложений скрыта от текущего пользователя (список неполный). Пустой
            ``attachments`` означает отсутствие видимых вложений у активности.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                result = await ips.wf_attachments(48210)  # 48210 = activityId
                for att in result.attachments:
                    print(att.object_id, att.caption)
                if result.has_invisible_items:
                    print("часть вложений скрыта по правам")

        Notes:
            operationId ``WFAttachments_GetAttachmments``; путь
            ``GET /core/api/wfAttachments/{activityId}/getAttachmments`` (опечатка
            «Attachmments» — в самом API). См. [[ips-object-model]].
        """
        path = f"/core/api/wfAttachments/{activity_id}/getAttachmments"
        data = await self._request("get", path)
        return AttachmentsList.model_validate(data)
