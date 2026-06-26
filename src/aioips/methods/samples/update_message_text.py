"""Метод обновления текста демо-сообщения (samples)."""

from typing import Any

from ...core import APIManager


class UpdateMessageTextMixin(APIManager):
    """Реализует ``POST /core/api/samples/messages/{id}/updates/text`` (``Messages_UpdateText``)."""

    async def update_message_text(
        self: "UpdateMessageTextMixin",
        message_id: int,
        text: str,
        *,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Обновляет только текст демо-сообщения учебного раздела ``samples`` (мутация).

        Раздел ``samples`` — демонстрационный (учебный) API; на доменные объекты IPS
        не влияет. Точечная мутация (меняет только текст), защищена гейтом: без
        ``confirm=True`` метод не делает запрос и поднимает :class:`ValueError`. Для
        полной замены сообщения используйте :meth:`update_message`.

        Args:
            message_id: Идентификатор сообщения (подставляется в путь ``/messages/{id}``).
            text: Новый текст сообщения. Передаётся обязательным query-параметром
                ``text`` (тело запроса пустое, ``json={}``).
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
                await ips.update_message_text(1, "новый текст", confirm=True)

        Notes:
            operationId ``Messages_UpdateText``; путь
            ``POST /core/api/samples/messages/{id}/updates/text`` (query ``text``, тело
            пустое, ответ ``FullMessageDTO``). Связанный метод: :meth:`update_message`.
        """
        if confirm is not True:
            raise ValueError(
                "Изменение текста демо-сообщения меняет состояние: передайте confirm=True"
            )
        data = await self._request(
            "post",
            f"/core/api/samples/messages/{message_id}/updates/text",
            json={},
            params={"text": text},
        )
        return dict(data)
