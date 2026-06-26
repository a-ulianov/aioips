"""Метод получения сообщений обсуждений по их идентификаторам."""

from ...core import APIManager
from ...schemas.discussions import Message, MessageId


class GetMessagesMixin(APIManager):
    """Реализует ``GET /core/api/discussions/getMessages`` (``Discussions_GetMessages``)."""

    async def get_messages(
        self: "GetMessagesMixin",
        message_ids: list[MessageId],
    ) -> list[Message]:
        """Возвращает сообщения обсуждений по списку их идентификаторов.

        Дозагружает полные сообщения по их составным идентификаторам
        (:class:`MessageId`): применяют, когда уже известны идентификаторы сообщений
        (например, получены из :meth:`find_messages` или :meth:`get_messages_by_id`) и
        нужно получить их актуальное содержимое. Для выборки всех сообщений одного
        обсуждения используйте :meth:`get_messages_by_id`, для сообщений конкретной
        версии объекта — :meth:`find_messages`.

        Предусловие: идентификаторы передаются телом запроса; ``MessageId`` —
        составной (версия сообщения + момент создания + GUID версии автора), его
        обычно берут из ответа другого метода раздела, а не конструируют вручную.

        Args:
            message_ids: Список составных идентификаторов сообщений
                (:class:`MessageId`), которые требуется загрузить. Пустой список —
                сервер вернёт пустой результат.

        Returns:
            Список сообщений по схеме :class:`Message` в том же составе, что запрошен.
            Пустой список означает, что сообщений с такими идентификаторами нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                found = await ips.find_messages(279514)
                full = await ips.get_messages([m.id for m in found])
                for msg in full:
                    print(msg.caption, msg.author_name)

        Notes:
            ``operationId``: ``Discussions_GetMessages``; путь
            ``GET /core/api/discussions/getMessages`` (тело — массив ``MessageIdDto``,
            ответ — массив ``MessageDto``).
        """
        body = [m.model_dump(mode="json", by_alias=True, exclude_none=True) for m in message_ids]
        data = await self._request("get", "/core/api/discussions/getMessages", json=body)
        return [Message.model_validate(item) for item in data]
