"""Метод получения пользовательского действия запуска IPS Bridge."""

from typing import Any

from ...core import APIManager
from ...schemas.bridge import LaunchActionInfo


class BridgeUserDefinedLaunchActionMixin(APIManager):
    """Реализует ``GET /core/api/Bridge/Launch/GetUserDefinedLaunchAction``.

    ``operationId``: ``Bridge_GetUserDefinedLaunchAction``.
    """

    async def bridge_user_defined_launch_action(
        self: "BridgeUserDefinedLaunchActionMixin",
        *,
        object_type_id: int | None = None,
        launch_type: int | None = None,
    ) -> LaunchActionInfo:
        """Возвращает пользовательское действие запуска для типа объекта и режима.

        Действие запуска (launch action) описывает операцию, которую IPS Bridge
        выполняет над объектом на стороне клиента. Метод подбирает пользовательское
        (настроенное администратором) действие по типу объекта и виду запуска.
        Применяйте, чтобы узнать, какое действие сработает для объекта данного типа;
        его данные получают через :meth:`bridge_launch_action_data`. Предусловий нет.

        Args:
            object_type_id: Идентификатор типа объекта, для которого ищется
                действие. ``None`` (по умолчанию) — параметр не передаётся.
            launch_type: Числовой код режима запуска. ``None`` (по умолчанию) —
                параметр не передаётся.

        Returns:
            Действие запуска по схеме :class:`LaunchActionInfo` с полями
            ``action_id``, ``handler_id`` и ``display_name``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                action = await ips.bridge_user_defined_launch_action(
                    object_type_id=1,
                    launch_type=0,
                )
                print(action.action_id, action.display_name)

        Notes:
            ``operationId``: ``Bridge_GetUserDefinedLaunchAction``; путь
            ``GET /core/api/Bridge/Launch/GetUserDefinedLaunchAction``. Ключи query —
            ``objectTypeId``, ``launchType``.
        """
        params: dict[str, Any] = {}
        if object_type_id is not None:
            params["objectTypeId"] = object_type_id
        if launch_type is not None:
            params["launchType"] = launch_type
        data = await self._request(
            "get", "/core/api/Bridge/Launch/GetUserDefinedLaunchAction", params=params
        )
        return LaunchActionInfo.model_validate(data)
