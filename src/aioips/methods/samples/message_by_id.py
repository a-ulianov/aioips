"""Метод получения демо-сообщения по идентификатору (samples)."""

from typing import Any

from ...core import APIManager


class MessageByIdMixin(APIManager):
    """Реализует ``GET /core/api/samples/messages/{id}`` (``Messages_GetById``)."""

    async def message_by_id(self: "MessageByIdMixin", message_id: int) -> dict[str, Any]:
        """Возвращает одно демо-сообщение учебного раздела ``samples`` по идентификатору.

        Раздел ``samples`` — демонстрационный (учебный) API сообщений; на доменные
        объекты IPS не влияет. Применяйте, когда известен идентификатор сообщения
        (например, из :meth:`messages` или ответа :meth:`add_sample_message`) и нужно получить
        его актуальное состояние. Для всего набора используйте :meth:`messages`.

        Args:
            message_id: Идентификатор сообщения (``id`` из ``FullMessageDTO``, >= 1).
                Подставляется в путь ``/messages/{id}``.

        Returns:
            Сообщение (``FullMessageDTO``) как ``dict[str, Any]`` с ключами ``id``,
            ``createTime``, ``lastWriteTime``, ``text``. Для типизированного разбора см.
            :class:`aioips.schemas.samples.FullMessage`.

        Raises:
            IPSNotFoundError: Если сообщения с таким идентификатором нет.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                msg = await ips.message_by_id(1)
                print(msg["text"])

        Notes:
            operationId ``Messages_GetById``; путь
            ``GET /core/api/samples/messages/{id}`` (объект ``FullMessageDTO``).
            Связанные методы: :meth:`messages`, :meth:`update_message`.
        """
        data = await self._request("get", f"/core/api/samples/messages/{message_id}")
        return dict(data)
