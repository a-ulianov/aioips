"""Метод удаления демо-сообщения (samples)."""

from ...core import APIManager


class DeleteMessageMixin(APIManager):
    """Реализует ``DELETE /core/api/samples/messages/{id}`` (``Messages_Delete``)."""

    async def delete_message(
        self: "DeleteMessageMixin",
        message_id: int,
        *,
        confirm: bool = False,
    ) -> None:
        """Удаляет демо-сообщение учебного раздела ``samples`` (РАЗРУШАЮЩАЯ операция).

        Раздел ``samples`` — демонстрационный (учебный) API; на доменные объекты IPS
        не влияет. Удаление необратимо, поэтому по умолчанию НЕ выполняется: требуется
        явный ``confirm=True``, иначе поднимается :class:`ValueError` ещё ДО обращения к
        серверу. Это обратная операция к :meth:`add_sample_message` (удаляет ранее созданное
        сообщение по его ``id``).

        Args:
            message_id: Идентификатор удаляемого сообщения (подставляется в путь
                ``/messages/{id}``), обычно ``id`` из ответа :meth:`add_sample_message` или из
                :meth:`messages`.
            confirm: Подтверждение разрушающей операции. Без ``True`` метод не делает
                запрос и поднимает :class:`ValueError` (защитный гейт).

        Returns:
            ``None``. Сервер возвращает пустой ответ (``void``).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSNotFoundError: Если сообщения с таким идентификатором нет.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                created = await ips.add_sample_message(
                    {"id": 0, "text": "x"}, confirm=True
                )
                await ips.delete_message(created["id"], confirm=True)

        Notes:
            operationId ``Messages_Delete``; путь
            ``DELETE /core/api/samples/messages/{id}`` (ответ ``void``). Обратный метод:
            :meth:`add_sample_message`.
        """
        if confirm is not True:
            raise ValueError("Удаление демо-сообщения необратимо: передайте confirm=True")
        await self._request("delete", f"/core/api/samples/messages/{message_id}")
