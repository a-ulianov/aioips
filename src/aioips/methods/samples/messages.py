"""Метод получения всех демо-сообщений (samples)."""

from typing import Any

from ...core import APIManager


class MessagesMixin(APIManager):
    """Реализует ``GET /core/api/samples/messages`` (``Messages_GetAll``)."""

    async def messages(self: "MessagesMixin") -> list[dict[str, Any]]:
        """Возвращает все демо-сообщения учебного раздела ``samples``.

        Раздел ``samples`` — демонстрационный (учебный) API сообщений/уведомлений: он
        не затрагивает доменные объекты IPS и служит для проверки соединения,
        авторизации и примеров работы клиента. Этот метод отдаёт полный список
        сообщений без фильтрации.

        Когда применять: чтобы получить весь набор демо-сообщений (например, после
        :meth:`add_sample_message`). Для отбора по тексту/времени используйте
        :meth:`messages_by_filter`; для одного сообщения по идентификатору —
        :meth:`message_by_id`. Предусловий нет; операция идемпотентна.

        Returns:
            Список сообщений (``FullMessageDTO``) как ``list[dict[str, Any]]``. Каждый
            элемент содержит ключи ``id``, ``createTime``, ``lastWriteTime``, ``text``.
            Пустой список означает, что сообщений нет. Для типизированного разбора см.
            :class:`aioips.schemas.samples.FullMessage`.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                items = await ips.messages()
                for msg in items:
                    print(msg["id"], msg["text"])

        Notes:
            operationId ``Messages_GetAll``; путь ``GET /core/api/samples/messages``
            (массив ``FullMessageDTO``). Связанные методы: :meth:`message_by_id`,
            :meth:`messages_by_filter`, :meth:`add_sample_message`.
        """
        data = await self._request("get", "/core/api/samples/messages")
        return list(data) if data is not None else []
