"""Метод получения сообщений конкретного обсуждения по его версии."""

from ...core import APIManager
from ...schemas.discussions import Message


class GetMessagesByIdMixin(APIManager):
    """Реализует ``GET /core/api/discussions/{discussionVersionId}/getMessagesById``.

    ``operationId``: ``Discussions_GetMessagesById``.
    """

    async def get_messages_by_id(
        self: "GetMessagesByIdMixin",
        discussion_version_id: int,
    ) -> list[Message]:
        """Возвращает все сообщения одного обсуждения по идентификатору его версии.

        Загружает поток сообщений конкретного обсуждения (нить переписки целиком).
        Идентификатор обсуждения берётся из поля ``id.discussion_version_id`` сообщений,
        полученных через :meth:`get_messages` или :meth:`find_messages`.

        Предусловие по id-пространству (критично): аргумент — это идентификатор ВЕРСИИ
        обсуждения (``discussionVersionId`` из :class:`MessageId`), а НЕ версия объекта
        и не идентификатор объекта.

        Args:
            discussion_version_id: Идентификатор ВЕРСИИ обсуждения
                (``discussionVersionId`` из ``Message.id``).

        Returns:
            Список сообщений обсуждения по схеме :class:`Message`. Пустой список
            означает, что обсуждение не содержит сообщений (или не найдено).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                feed = await ips.get_messages()
                if feed:
                    thread = await ips.get_messages_by_id(feed[0].id.discussion_version_id)

        Notes:
            ``operationId``: ``Discussions_GetMessagesById``; путь
            ``GET /core/api/discussions/{discussionVersionId}/getMessagesById``
            (массив ``MessageDto``).
        """
        path = f"/core/api/discussions/{discussion_version_id}/getMessagesById"
        data = await self._request("get", path)
        return [Message.model_validate(item) for item in data]
