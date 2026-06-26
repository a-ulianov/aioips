"""Метод получения действий запуска по умолчанию IPS Bridge."""

from typing import Any

from ...core import APIManager


class BridgeGetDefaultActionsMixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Launch/GetDefaultActions``.

    ``operationId``: ``Bridge_GetDefaultActions``.
    """

    async def bridge_get_default_actions(
        self: "BridgeGetDefaultActionsMixin",
        *,
        object_type_id: int | None = None,
        user_id: int | None = None,
    ) -> list[dict[str, Any]]:
        """Возвращает действия запуска ПО УМОЛЧАНИЮ для типа объекта и пользователя.

        IPS Bridge — серверный помощник десктоп-клиента; действие запуска
        (launch action) описывает операцию над объектом на стороне клиента.
        Метод отдаёт действия, назначенные по умолчанию для данного типа объекта
        (и, опционально, пользователя), с указанием режима запуска. Это операция
        ЧТЕНИЯ — подтверждения не требует. Назначить действие по умолчанию —
        :meth:`bridge_set_default_action`, сбросить —
        :meth:`bridge_reset_default_action`. Предусловий нет.

        Args:
            object_type_id: Идентификатор типа объекта. ``None`` — параметр не
                передаётся.
            user_id: Идентификатор пользователя. ``None`` — параметр не передаётся
                (действия по умолчанию для всех).

        Returns:
            Список словарей вида ``LaunchActionInfoWithType`` с ключами
            ``actionInfo`` (сведения о действии) и ``launchType`` (режим запуска).
            Пустой список ``[]``, если действий нет или сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                defaults = await ips.bridge_get_default_actions(object_type_id=1)

        Notes:
            ``operationId``: ``Bridge_GetDefaultActions``; путь
            ``POST /core/api/Bridge/Launch/GetDefaultActions``. Ключи query —
            ``objectTypeId``, ``userId``. Тело не передаётся (``{}`` против 415).
            Структура элемента сложная (вложенный ``actionInfo``), поэтому
            возвращается ``dict``, а не типизированная модель.
        """
        params: dict[str, Any] = {}
        if object_type_id is not None:
            params["objectTypeId"] = object_type_id
        if user_id is not None:
            params["userId"] = user_id
        data = await self._request(
            "post", "/core/api/Bridge/Launch/GetDefaultActions", params=params, json={}
        )
        items = data if isinstance(data, list) else []
        return [dict(item) for item in items]
