"""Метод удаления сообщения обсуждения."""

from ...core import APIManager
from ...schemas.discussions import MessageId


class RemoveMessageMixin(APIManager):
    """Реализует ``POST /core/api/discussions/removeMessage`` (``Discussions_RemoveMessage``)."""

    async def remove_message(
        self: "RemoveMessageMixin",
        message_id: MessageId,
        *,
        confirm: bool = False,
    ) -> bool:
        """Удаляет сообщение обсуждения (РАЗРУШАЮЩАЯ операция, защищена ``confirm``).

        Безвозвратно удаляет сообщение из обсуждения. Поскольку операция необратима,
        по умолчанию НЕ выполняется: требуется явный ``confirm=True``, иначе
        поднимается :class:`ValueError` ещё ДО обращения к серверу. Применяйте для
        удаления ранее созданного (:meth:`add_message`) или отредактированного
        (:meth:`edit_message`) сообщения. Идентификатор удаляемого сообщения обычно
        получают из :meth:`find_messages` или :meth:`get_messages`, а не конструируют
        вручную.

        Предусловие по id-пространству (критично): ``message_id`` — составной
        идентификатор сообщения (:class:`MessageId`: версия записи сообщения + момент
        создания + GUID версии автора), он передаётся ТЕЛОМ запроса (``MessageIdDto``).

        Args:
            message_id: Составной идентификатор удаляемого сообщения
                (:class:`MessageId`), полученный из :meth:`find_messages` или
                :meth:`get_messages`.
            confirm: Подтверждение разрушающей операции. Без ``True`` метод не делает
                запрос и поднимает :class:`ValueError` (защитный гейт).

        Returns:
            ``True``, если сервер подтвердил удаление; ``False`` — если ответ пуст
            или отрицателен.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При иной ошибке сервера (например, сообщение не найдено).

        Example:
            async with IPSClient(config=config) as ips:
                found = await ips.find_messages(102550)
                await ips.remove_message(found[0].id, confirm=True)

        Notes:
            ``operationId``: ``Discussions_RemoveMessage``; путь
            ``POST /core/api/discussions/removeMessage`` (тело ``MessageIdDto``;
            ответ — булево).
        """
        if confirm is not True:
            raise ValueError(
                "Удаление сообщения необратимо: передайте confirm=True для подтверждения"
            )
        body = message_id.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/discussions/removeMessage", json=body)
        return bool(data) if data is not None else False
