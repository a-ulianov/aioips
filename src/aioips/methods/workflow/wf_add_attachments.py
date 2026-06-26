"""Метод добавления вложений к активности процесса."""

from ...core import APIManager
from ...schemas.workflow import AttachmentsList


class WFAddAttachmentsMixin(APIManager):
    """Реализует ``POST /core/api/wfAttachments/{activityId}/addAttachmments``.

    operationId ``WFAttachments_AddAttachmments`` (двойная «m» — опечатка в самом API).
    """

    async def wf_add_attachments(
        self: "WFAddAttachmentsMixin",
        activity_id: int,
        attachment_ids: list[int],
    ) -> AttachmentsList:
        """Прикрепляет объекты к активности (задаче) процесса как вложения.

        Вложения активности workflow — это объекты IPS, привязанные к шагу маршрута.
        Метод добавляет указанные объекты во вложения активности и возвращает
        обновлённый список — МУТИРУЮЩАЯ операция. Применяйте, чтобы приложить документы
        к задаче; текущий состав вложений читает :meth:`wf_attachments`, удаляет —
        :meth:`wf_remove_attachments`, а допустимые типы объектов-вложений даёт
        :meth:`wf_attachment_allowed_types`.

        Предусловие по id-пространству: ``activity_id`` — идентификатор АКТИВНОСТИ
        (задачи) экземпляра процесса, а элементы ``attachment_ids`` — идентификаторы
        ОБЪЕКТОВ (``objectID`` / F_OBJECT_ID), а не версий.

        Args:
            activity_id: Идентификатор активности (задачи) экземпляра процесса workflow.
            attachment_ids: Идентификаторы ОБЪЕКТОВ-вложений (``objectID``), которые
                нужно прикрепить. Передаются телом запроса как голый JSON-массив
                целых чисел.

        Returns:
            :class:`AttachmentsList`: обновлённый список вложений активности (поле
            ``attachments``) и признак наличия скрытых от пользователя элементов
            (``has_invisible_items``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                result = await ips.wf_add_attachments(48210, [102550])  # 48210 = activityId
                for att in result.attachments:
                    print(att.object_id, att.caption)

        Notes:
            operationId ``WFAttachments_AddAttachmments``; путь
            ``POST /core/api/wfAttachments/{activityId}/addAttachmments`` (двойная «m» в
            ``addAttachmments`` — опечатка в самом API). Тело — голый JSON-массив
            ``int``. Связанные методы: :meth:`wf_attachments`,
            :meth:`wf_remove_attachments`, :meth:`wf_attachments_data`. См.
            [[ips-object-model]].
        """
        path = f"/core/api/wfAttachments/{activity_id}/addAttachmments"
        data = await self._request("post", path, json=attachment_ids)
        return AttachmentsList.model_validate(data)
