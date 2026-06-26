"""Метод получения истории изменений сессии IPS Bridge."""

from typing import Any

from ...core import APIManager


class BridgeGetModificationsHistoryListMixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Session/GetModificationsHistoryList``.

    ``operationId``: ``Bridge_GetModificationsHistoryList``.
    """

    async def bridge_get_modifications_history_list(
        self: "BridgeGetModificationsHistoryListMixin",
    ) -> list[dict[str, Any]]:
        """Возвращает список изменений, накопленных за время логирования сессии.

        IPS Bridge — серверный помощник десктоп-клиента; он может вести журнал
        истории изменений сессии. Метод отдаёт накопленные записи (категория,
        идентификатор, тип действия). Это операция ЧТЕНИЯ — подтверждения не
        требует. Логирование включается :meth:`bridge_start_log_history` и
        выключается :meth:`bridge_stop_log_history`; этот метод читает то, что
        попало в журнал между ними. Предусловие: для непустого результата
        логирование должно было быть запущено.

        Returns:
            Список словарей вида ``CategoryValue`` с ключами ``categoryType``,
            ``categoryID`` и ``actionID``. Пустой список ``[]``, если изменений
            нет или сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.bridge_start_log_history(confirm=True)
                # ... операции клиента ...
                history = await ips.bridge_get_modifications_history_list()

        Notes:
            ``operationId``: ``Bridge_GetModificationsHistoryList``; путь
            ``POST /core/api/Bridge/Session/GetModificationsHistoryList``. Тело не
            передаётся (``{}`` против 415). Структура элемента включает enum
            ``actionID``, поэтому возвращается ``dict``, а не типизированная модель.
        """
        data = await self._request(
            "post", "/core/api/Bridge/Session/GetModificationsHistoryList", json={}
        )
        items = data if isinstance(data, list) else []
        return [dict(item) for item in items]
