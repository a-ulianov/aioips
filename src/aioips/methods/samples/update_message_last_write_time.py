"""Метод обновления времени изменения демо-сообщения (samples)."""

from typing import Any

from ...core import APIManager


class UpdateMessageLastWriteTimeMixin(APIManager):
    """Реализует ``POST /core/api/samples/messages/{id}/updates/lastWriteTime``.

    operationId ``Messages_UpdateLastWriteTime``.
    """

    async def update_message_last_write_time(
        self: "UpdateMessageLastWriteTimeMixin",
        message_id: int,
        last_write_time: str,
        *,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Обновляет время последнего изменения демо-сообщения ``samples`` (мутация).

        Раздел ``samples`` — демонстрационный (учебный) API; на доменные объекты IPS
        не влияет. Точечная мутация (меняет только ``lastWriteTime``), защищена гейтом:
        без ``confirm=True`` метод не делает запрос и поднимает :class:`ValueError`. Для
        полной замены сообщения используйте :meth:`update_message`.

        Args:
            message_id: Идентификатор сообщения (подставляется в путь ``/messages/{id}``).
            last_write_time: Новое время изменения в формате ISO-8601 ``date-time``
                (UTC). Передаётся обязательным query-параметром ``lastWriteTime`` (тело
                запроса пустое, ``json={}``).
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
                await ips.update_message_last_write_time(
                    1, "2026-06-25T12:00:00Z", confirm=True
                )

        Notes:
            operationId ``Messages_UpdateLastWriteTime``; путь
            ``POST /core/api/samples/messages/{id}/updates/lastWriteTime`` (query
            ``lastWriteTime``, тело пустое, ответ ``FullMessageDTO``). Связанный метод:
            :meth:`update_message`.
        """
        if confirm is not True:
            raise ValueError(
                "Изменение времени демо-сообщения меняет состояние: передайте confirm=True"
            )
        data = await self._request(
            "post",
            f"/core/api/samples/messages/{message_id}/updates/lastWriteTime",
            json={},
            params={"lastWriteTime": last_write_time},
        )
        return dict(data)
