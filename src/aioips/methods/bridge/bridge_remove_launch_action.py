"""Метод удаления действия запуска IPS Bridge (мутация)."""

from typing import Any

from ...core import APIManager


class BridgeRemoveLaunchActionMixin(APIManager):
    """Реализует ``DELETE /core/api/Bridge/Launch/RemoveLaunchAction``.

    ``operationId``: ``Bridge_RemoveLaunchAction``.
    """

    async def bridge_remove_launch_action(
        self: "BridgeRemoveLaunchActionMixin",
        *,
        action_id: str | None = None,
        confirm: bool = False,
    ) -> None:
        """Удаляет действие запуска IPS Bridge по его идентификатору (МУТАЦИЯ).

        IPS Bridge — серверный помощник десктоп-клиента; действие запуска
        (launch action) описывает операцию над объектом на стороне клиента.
        Метод удаляет действие по его GUID. Парное удаление к
        :meth:`bridge_create_launch_action`.

        Обратимость: операция НЕОБРАТИМА — удалённое действие нужно создавать
        заново через :meth:`bridge_create_launch_action`.

        Защита: удаление защищено ``confirm`` — без ``confirm=True`` поднимается
        :class:`ValueError` ещё ДО обращения к серверу (запрос не выполняется).

        Args:
            action_id: GUID действия запуска. ``None`` — параметр не передаётся.
            confirm: Подтверждение удаления. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие
            ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (404, если действие не найдено).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.bridge_remove_launch_action(
                    action_id="cad001c5-306c-11d8-b4e9-00304f19f545", confirm=True,
                )

        Notes:
            ``operationId``: ``Bridge_RemoveLaunchAction``; путь
            ``DELETE /core/api/Bridge/Launch/RemoveLaunchAction``. Ключ query —
            ``actionId``.
        """
        if confirm is not True:
            raise ValueError(
                "bridge_remove_launch_action удаляет действие на сервере; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if action_id is not None:
            params["actionId"] = action_id
        await self._request("delete", "/core/api/Bridge/Launch/RemoveLaunchAction", params=params)
        return None
