"""Метод получения полного списка действий запуска IPS Bridge."""

from typing import Any

from ...core import APIManager


class BridgeGetFullActionListMixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Launch/GetFullActionList``.

    ``operationId``: ``Bridge_GetFullActionList``.
    """

    async def bridge_get_full_action_list(
        self: "BridgeGetFullActionListMixin",
        *,
        object_type_id: int | None = None,
        user_id: int | None = None,
    ) -> list[dict[str, Any]]:
        """Возвращает ПОЛНЫЙ список действий запуска для типа объекта и пользователя.

        IPS Bridge — серверный помощник десктоп-клиента; действие запуска
        (launch action) описывает операцию над объектом на стороне клиента.
        В отличие от :meth:`bridge_get_action_list`, метод отдаёт все доступные
        действия с указанием их режима запуска (edit/view/print). Это операция
        ЧТЕНИЯ — подтверждения не требует. Предусловий нет.

        Args:
            object_type_id: Идентификатор типа объекта. ``None`` — параметр не
                передаётся.
            user_id: Идентификатор пользователя. ``None`` — параметр не передаётся.

        Returns:
            Список словарей вида ``LaunchActionInfoWithType`` с ключами
            ``actionInfo`` (сведения о действии) и ``launchType`` (режим запуска).
            Пустой список ``[]``, если действий нет или сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                actions = await ips.bridge_get_full_action_list(
                    object_type_id=1, user_id=7,
                )

        Notes:
            ``operationId``: ``Bridge_GetFullActionList``; путь
            ``POST /core/api/Bridge/Launch/GetFullActionList``. Ключи query —
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
            "post", "/core/api/Bridge/Launch/GetFullActionList", params=params, json={}
        )
        items = data if isinstance(data, list) else []
        return [dict(item) for item in items]
