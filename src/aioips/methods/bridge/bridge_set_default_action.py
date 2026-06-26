"""Метод назначения действия запуска по умолчанию IPS Bridge (мутация)."""

from typing import Any

from ...core import APIManager


class BridgeSetDefaultActionMixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Launch/SetDefaultAction``.

    ``operationId``: ``Bridge_SetDefaultAction``.
    """

    async def bridge_set_default_action(
        self: "BridgeSetDefaultActionMixin",
        *,
        object_type_id: int | None = None,
        action_id: str | None = None,
        user_id: int | None = None,
        confirm: bool = False,
    ) -> None:
        """Назначает действие запуска ПО УМОЛЧАНИЮ для типа объекта (МУТАЦИЯ).

        IPS Bridge — серверный помощник десктоп-клиента; действие запуска
        (launch action) описывает операцию над объектом на стороне клиента.
        Метод делает указанное действие действием по умолчанию для типа объекта
        (и, опционально, пользователя). Прочитать текущие умолчания —
        :meth:`bridge_get_default_actions`, сбросить —
        :meth:`bridge_reset_default_action`.

        Обратимость: операция ОБРАТИМА — назначение снимается парным
        :meth:`bridge_reset_default_action` с теми же ключами.

        Защита: меняет настройки на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            object_type_id: Идентификатор типа объекта. ``None`` — не передаётся.
            action_id: GUID назначаемого действия. ``None`` — не передаётся.
            user_id: Идентификатор пользователя. ``None`` — не передаётся
                (умолчание для всех).
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие
            ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.bridge_set_default_action(
                    object_type_id=1,
                    action_id="cad001c5-306c-11d8-b4e9-00304f19f545",
                    confirm=True,
                )

        Notes:
            ``operationId``: ``Bridge_SetDefaultAction``; путь
            ``POST /core/api/Bridge/Launch/SetDefaultAction``. Ключи query —
            ``objectTypeId``, ``actionId``, ``userId``. Тело не передаётся
            (``{}`` против 415).
        """
        if confirm is not True:
            raise ValueError(
                "bridge_set_default_action меняет действие по умолчанию; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if object_type_id is not None:
            params["objectTypeId"] = object_type_id
        if action_id is not None:
            params["actionId"] = action_id
        if user_id is not None:
            params["userId"] = user_id
        await self._request(
            "post", "/core/api/Bridge/Launch/SetDefaultAction", params=params, json={}
        )
        return None
