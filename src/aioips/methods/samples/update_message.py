"""Метод обновления демо-сообщения (samples)."""

from typing import Any

from ...core import APIManager


class UpdateMessageMixin(APIManager):
    """Реализует ``PUT /core/api/samples/messages/{id}`` (``Messages_Update``)."""

    async def update_message(
        self: "UpdateMessageMixin",
        message_id: int,
        message: dict[str, Any],
        *,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Полностью обновляет демо-сообщение учебного раздела ``samples`` (мутация).

        Раздел ``samples`` — демонстрационный (учебный) API; на доменные объекты IPS
        не влияет. Операция изменяет состояние сервера, поэтому защищена гейтом: без
        ``confirm=True`` метод не делает запрос и поднимает :class:`ValueError`.
        Заменяет сообщение целиком; для точечных изменений есть
        :meth:`update_message_text` и :meth:`update_message_last_write_time`.

        Args:
            message_id: Идентификатор обновляемого сообщения (подставляется в путь
                ``/messages/{id}``).
            message: Полное тело ``FullMessageDTO`` как ``dict`` с ключами ``id``,
                ``createTime``, ``lastWriteTime``, ``text``. Типизированно сформировать
                можно через :class:`aioips.schemas.samples.FullMessage`
                (``model_dump(by_alias=True)``).
            confirm: Подтверждение мутации. Без ``True`` запрос не выполняется
                (защитный гейт).

        Returns:
            Обновлённое сообщение (``FullMessageDTO``) как ``dict[str, Any]``.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSNotFoundError: Если сообщения с таким идентификатором нет.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                msg = await ips.message_by_id(1)
                msg["text"] = "исправлено"
                await ips.update_message(1, msg, confirm=True)

        Notes:
            operationId ``Messages_Update``; путь
            ``PUT /core/api/samples/messages/{id}`` (тело и ответ — ``FullMessageDTO``).
            Связанные методы: :meth:`update_message_text`,
            :meth:`update_message_last_write_time`.
        """
        if confirm is not True:
            raise ValueError("Обновление демо-сообщения меняет состояние: передайте confirm=True")
        data = await self._request(
            "put",
            f"/core/api/samples/messages/{message_id}",
            json=message,
        )
        return dict(data)
