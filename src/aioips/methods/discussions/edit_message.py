"""Метод редактирования сообщения обсуждения."""

from typing import Any

from ...core import APIManager
from ...schemas.discussions import Message, MessageId


class EditMessageMixin(APIManager):
    """Реализует ``POST /core/api/discussions/editMessage`` (``Discussions_EditMessage``)."""

    async def edit_message(
        self: "EditMessageMixin",
        message_id: MessageId,
        *,
        caption: str | None = None,
        text: str | None = None,
    ) -> Message:
        """Редактирует существующее сообщение обсуждения (МУТИРУЮЩАЯ операция).

        Изменяет заголовок и/или текст ранее созданного сообщения и возвращает его
        обновлённое состояние. Применяйте для правки уже существующего сообщения
        (создание нового — :meth:`add_message`). Идентификатор адресуемого сообщения
        обычно получают из :meth:`find_messages` или :meth:`get_messages`, а не
        конструируют вручную.

        Предусловие по id-пространству (критично): ``message_id`` — составной
        идентификатор сообщения (:class:`MessageId`: версия записи сообщения + момент
        создания + GUID версии автора), он передаётся ТЕЛОМ запроса (``MessageIdDto``).
        Новые ``caption``/``text`` передаются строкой запроса; передавайте только те,
        что нужно изменить — незаданные (``None``) в запрос не попадают. Сообщение
        должно быть доступно для правки (см. флаги ``is_read_only``/``is_reply_only``
        в :class:`Message`).

        Args:
            message_id: Составной идентификатор редактируемого сообщения
                (:class:`MessageId`), полученный из :meth:`find_messages` или
                :meth:`get_messages`.
            caption: Новый заголовок сообщения. ``None`` — параметр не передаётся.
            text: Новый текст сообщения. ``None`` — параметр не передаётся.

        Returns:
            Обновлённое сообщение по схеме :class:`Message`.

        Raises:
            IPSError: При ошибочном ответе сервера (например, сообщение только для
                чтения или не найдено).

        Example:
            async with IPSClient(config=config) as ips:
                found = await ips.find_messages(102550)
                edited = await ips.edit_message(
                    found[0].id,
                    text="Размеры на листе 2 уточнены.",
                )
                print(edited.last_modification_timestamp)

        Notes:
            ``operationId``: ``Discussions_EditMessage``; путь
            ``POST /core/api/discussions/editMessage`` (тело ``MessageIdDto``,
            query ``caption``, ``text``; ответ — ``MessageDto``).
        """
        params: dict[str, Any] = {}
        if caption is not None:
            params["caption"] = caption
        if text is not None:
            params["text"] = text
        body = message_id.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post", "/core/api/discussions/editMessage", json=body, params=params
        )
        return Message.model_validate(data)
