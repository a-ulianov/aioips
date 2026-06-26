"""Метод получения сведений о действии запуска IPS Bridge."""

from typing import Any

from ...core import APIManager
from ...schemas.bridge import LaunchActionInfo


class BridgeLaunchActionInfoMixin(APIManager):
    """Реализует ``GET /core/api/Bridge/Launch/GetLaunchActionInfo``.

    ``operationId``: ``Bridge_GetLaunchActionInfo``.
    """

    async def bridge_launch_action_info(
        self: "BridgeLaunchActionInfoMixin",
        *,
        action_id: str | None = None,
    ) -> LaunchActionInfo:
        """Возвращает сведения о действии запуска IPS Bridge по его идентификатору.

        Действие запуска (launch action) описывает операцию, которую IPS Bridge
        выполняет над объектом на стороне клиента. Метод отдаёт метаданные действия
        (обработчик, отображаемое имя) по его GUID. Применяйте, когда идентификатор
        действия уже известен (например, из
        :meth:`bridge_user_defined_launch_action`), а полезную нагрузку получают
        через :meth:`bridge_launch_action_data`. Предусловий нет.

        Args:
            action_id: GUID действия запуска в строковом представлении. ``None``
                (по умолчанию) — параметр не передаётся.

        Returns:
            Действие запуска по схеме :class:`LaunchActionInfo` с полями
            ``action_id``, ``handler_id`` и ``display_name``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                action = await ips.bridge_launch_action_info(
                    action_id="cad001c5-306c-11d8-b4e9-00304f19f545",
                )
                print(action.display_name)

        Notes:
            ``operationId``: ``Bridge_GetLaunchActionInfo``; путь
            ``GET /core/api/Bridge/Launch/GetLaunchActionInfo``. Ключ query —
            ``actionId``.
        """
        params: dict[str, Any] = {}
        if action_id is not None:
            params["actionId"] = action_id
        data = await self._request(
            "get", "/core/api/Bridge/Launch/GetLaunchActionInfo", params=params
        )
        return LaunchActionInfo.model_validate(data)
