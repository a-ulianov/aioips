"""Метод очистки демо-сообщений (samples)."""

from ...core import APIManager


class ClearMessageUpdatesMixin(APIManager):
    """Реализует ``POST /core/api/samples/messages/updates/clear`` (``Messages_Clear``)."""

    async def clear_message_updates(
        self: "ClearMessageUpdatesMixin",
        *,
        confirm: bool = False,
    ) -> None:
        """Очищает все демо-сообщения учебного раздела ``samples`` (МАССОВАЯ операция).

        Раздел ``samples`` — демонстрационный (учебный) API; на доменные объекты IPS
        не влияет. Операция массовая и необратимая (удаляет накопленные сообщения),
        поэтому по умолчанию НЕ выполняется: требуется явный ``confirm=True``, иначе
        поднимается :class:`ValueError` ещё ДО обращения к серверу. Для удаления одного
        сообщения используйте :meth:`delete_message`.

        Args:
            confirm: Подтверждение массовой разрушающей операции. Без ``True`` метод не
                делает запрос и поднимает :class:`ValueError` (защитный гейт).

        Returns:
            ``None``. Сервер возвращает пустой ответ (``void``).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.clear_message_updates(confirm=True)

        Notes:
            operationId ``Messages_Clear``; путь
            ``POST /core/api/samples/messages/updates/clear`` (без тела, ответ
            ``void``). No-body POST отправляется как ``json={}``.
        """
        if confirm is not True:
            raise ValueError("Очистка демо-сообщений массовая и необратима: передайте confirm=True")
        await self._request("post", "/core/api/samples/messages/updates/clear", json={})
