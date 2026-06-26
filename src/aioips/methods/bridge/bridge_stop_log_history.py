"""Метод выключения журнала истории изменений сессии IPS Bridge (мутация)."""

from ...core import APIManager


class BridgeStopLogHistoryMixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Session/StopLogHistory``.

    ``operationId``: ``Bridge_StopLogHistory``.
    """

    async def bridge_stop_log_history(
        self: "BridgeStopLogHistoryMixin",
        *,
        confirm: bool = False,
    ) -> None:
        """Выключает журналирование истории изменений сессии IPS Bridge (МУТАЦИЯ).

        IPS Bridge — серверный помощник десктоп-клиента; он может вести журнал
        изменений сессии. Метод останавливает журналирование, ранее включённое
        :meth:`bridge_start_log_history`. Накопленные за это время записи читаются
        :meth:`bridge_get_modifications_history_list`.

        Обратимость: операция ОБРАТИМА — журналирование снова включается парным
        :meth:`bridge_start_log_history`.

        Защита: меняет состояние сессии на сервере, поэтому защищена ``confirm``
        — без ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие
            ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.bridge_stop_log_history(confirm=True)

        Notes:
            ``operationId``: ``Bridge_StopLogHistory``; путь
            ``POST /core/api/Bridge/Session/StopLogHistory``. Тело не передаётся
            (``{}`` против 415).
        """
        if confirm is not True:
            raise ValueError(
                "bridge_stop_log_history меняет состояние сессии; передайте confirm=True",
            )
        await self._request("post", "/core/api/Bridge/Session/StopLogHistory", json={})
        return None
