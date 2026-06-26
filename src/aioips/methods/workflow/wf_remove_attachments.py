"""Метод удаления вложений активности процесса."""

from ...core import APIManager


class WFRemoveAttachmentsMixin(APIManager):
    """Реализует ``POST /core/api/wfAttachments/{activityId}/removeAttachmments``.

    operationId ``WFAttachments_RemoveAttachmments`` (двойная «m» — опечатка в API).
    """

    async def wf_remove_attachments(
        self: "WFRemoveAttachmentsMixin",
        activity_id: int,
        attachment_ids: list[int],
        *,
        confirm: bool = False,
    ) -> None:
        """Открепляет вложения от активности процесса (необратимо, защищено ``confirm``).

        Удаляет указанные объекты из вложений активности (задачи) workflow — МУТИРУЮЩАЯ,
        необратимая операция: восстановить связь можно только повторным
        :meth:`wf_add_attachments`. Поэтому по умолчанию метод НЕ выполняется —
        требуется явный ``confirm=True``, иначе поднимается :class:`ValueError` ещё ДО
        обращения к серверу. Текущий состав вложений читает :meth:`wf_attachments`.

        Предусловие по id-пространству: ``activity_id`` — идентификатор АКТИВНОСТИ
        (задачи) экземпляра процесса, а элементы ``attachment_ids`` — идентификаторы
        ОБЪЕКТОВ-вложений (``objectID`` / F_OBJECT_ID), а не версий.

        Args:
            activity_id: Идентификатор активности (задачи) экземпляра процесса workflow.
            attachment_ids: Идентификаторы ОБЪЕКТОВ-вложений (``objectID``), которые
                нужно открепить. Передаются телом запроса как голый JSON-массив
                целых чисел.
            confirm: Подтверждение необратимой операции. Без ``True`` метод не делает
                запрос и поднимает :class:`ValueError` (защитный гейт).

        Returns:
            ``None``: сервер не возвращает тело (void).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При иной ошибке сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.wf_remove_attachments(48210, [102550], confirm=True)

        Notes:
            operationId ``WFAttachments_RemoveAttachmments``; путь
            ``POST /core/api/wfAttachments/{activityId}/removeAttachmments`` (двойная «m»
            в ``removeAttachmments`` — опечатка в самом API). Тело — голый JSON-массив
            ``int``; ответ — без тела. Связанные методы: :meth:`wf_attachments`,
            :meth:`wf_add_attachments`. См. [[ips-object-model]].
        """
        if confirm is not True:
            raise ValueError(
                "Открепление вложений необратимо: передайте confirm=True для подтверждения"
            )
        path = f"/core/api/wfAttachments/{activity_id}/removeAttachmments"
        await self._request("post", path, json=attachment_ids)
        return None
