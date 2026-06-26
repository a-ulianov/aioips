"""Метод добавления сообщения в обсуждение версии объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.discussions import Message


class AddMessageMixin(APIManager):
    """Реализует ``POST /core/api/discussions/addMessage`` (``Discussions_AddMessage``)."""

    async def add_message(
        self: "AddMessageMixin",
        object_version_id: int,
        *,
        caption: str | None = None,
        text: str | None = None,
    ) -> Message:
        """Добавляет новое сообщение в обсуждение версии объекта (МУТИРУЮЩАЯ операция).

        Создаёт сообщение в потоке обсуждения, привязанном к указанной ВЕРСИИ объекта,
        и возвращает созданную запись. Применяйте, когда нужно начать или продолжить
        обсуждение конкретной версии объекта. Возможность обсуждения проверяется заранее
        через :meth:`can_discuss`; прочитать уже существующие сообщения — через
        :meth:`find_messages` (по версии объекта) или :meth:`get_messages` (по
        идентификаторам). Это парный write-метод к перечисленным read-методам раздела.

        Предусловие по id-пространству (критично): ``object_version_id`` — это
        идентификатор ВЕРСИИ объекта (``objectVersionId`` / F_ID), а НЕ идентификатор
        объекта (``objectID`` / F_OBJECT_ID). Заголовок и текст передаются строкой
        запроса; тело запроса пустое (``{}``). Передавайте только нужные из
        ``caption``/``text`` — незаданные (``None``) в запрос не попадают.

        Args:
            object_version_id: Идентификатор ВЕРСИИ объекта (``objectVersionId``, F_ID),
                в обсуждение которой добавляется сообщение.
            caption: Заголовок (тема) сообщения. ``None`` — параметр не передаётся.
            text: Текст сообщения. ``None`` — параметр не передаётся.

        Returns:
            Созданное сообщение по схеме :class:`Message` (с присвоенным составным
            идентификатором :class:`MessageId` в поле ``id``).

        Raises:
            IPSError: При ошибочном ответе сервера (например, обсуждение недопустимо).

        Example:
            async with IPSClient(config=config) as ips:
                msg = await ips.add_message(
                    102550,
                    caption="Замечание по чертежу",
                    text="Проверьте размеры на листе 2.",
                )
                print(msg.id.discussion_version_id)

        Notes:
            ``operationId``: ``Discussions_AddMessage``; путь
            ``POST /core/api/discussions/addMessage`` (query ``objectVersionId``,
            ``caption``, ``text``; тело ``{}``; ответ — ``MessageDto``).
            См. объектной модели IPS (раздел «Идентичность: объект ≠ версия»).
        """
        params: dict[str, Any] = {"objectVersionId": str(object_version_id)}
        if caption is not None:
            params["caption"] = caption
        if text is not None:
            params["text"] = text
        data = await self._request(
            "post", "/core/api/discussions/addMessage", json={}, params=params
        )
        return Message.model_validate(data)
