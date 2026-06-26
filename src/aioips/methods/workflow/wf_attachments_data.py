"""Метод получения данных вложений по их идентификаторам."""

from ...core import APIManager
from ...schemas.workflow import AttachmentsList


class WFAttachmentsDataMixin(APIManager):
    """Реализует ``POST /core/api/wfAttachments/getAttachmmentsData``.

    operationId ``WFAttachments_GetAttachmentsData`` (двойная «m» в пути — опечатка API).
    """

    async def wf_attachments_data(
        self: "WFAttachmentsDataMixin",
        attachment_ids: list[int],
    ) -> AttachmentsList:
        """Возвращает данные вложений процесса по их идентификаторам.

        Загружает сведения об объектах-вложениях (тип, владелец, режим правки и пр.) по
        списку их идентификаторов — операция ЧТЕНИЯ (read), не привязана к конкретной
        активности. Применяйте, чтобы получить детали уже известных вложений, не
        запрашивая весь состав активности через :meth:`wf_attachments`. Изменяют состав
        вложений активности :meth:`wf_add_attachments` и :meth:`wf_remove_attachments`.

        Предусловие по id-пространству: элементы ``attachment_ids`` — идентификаторы
        ОБЪЕКТОВ-вложений (``objectID`` / F_OBJECT_ID), а не версий.

        Args:
            attachment_ids: Идентификаторы ОБЪЕКТОВ-вложений (``objectID``), данные
                которых нужно получить. Передаются телом запроса как голый JSON-массив
                целых чисел.

        Returns:
            :class:`AttachmentsList`: поле ``attachments`` — список вложений
            (:class:`Attachment`), ``has_invisible_items`` — признак наличия скрытых от
            пользователя элементов. Пустой ``attachments`` означает, что по
            идентификаторам не нашлось видимых вложений.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                result = await ips.wf_attachments_data([102550, 102551])
                for att in result.attachments:
                    print(att.object_id, att.caption)

        Notes:
            operationId ``WFAttachments_GetAttachmentsData``; путь
            ``POST /core/api/wfAttachments/getAttachmmentsData`` (двойная «m» в
            ``getAttachmmentsData`` — опечатка в самом API). Тело — голый JSON-массив
            ``int``. Связанные методы: :meth:`wf_attachments`,
            :meth:`wf_add_attachments`. См. объектной модели IPS.
        """
        path = "/core/api/wfAttachments/getAttachmmentsData"
        data = await self._request("post", path, json=attachment_ids)
        return AttachmentsList.model_validate(data)
