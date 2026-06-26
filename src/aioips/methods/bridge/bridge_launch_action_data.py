"""Метод получения данных действия запуска IPS Bridge."""

from typing import Any

from ...core import APIManager


class BridgeLaunchActionDataMixin(APIManager):
    """Реализует ``GET /core/api/Bridge/Launch/GetLaunchActionData``.

    ``operationId``: ``Bridge_GetLaunchActionData``.
    """

    async def bridge_launch_action_data(
        self: "BridgeLaunchActionDataMixin",
        *,
        action_id: str | None = None,
    ) -> str:
        """Возвращает полезные данные действия запуска IPS Bridge по идентификатору.

        Данные действия запуска — сериализованная конфигурация (как правило, строка
        или XML), которую обработчик моста использует для выполнения операции над
        объектом. Метод отдаёт эти данные как строку по GUID действия. Применяйте,
        когда идентификатор действия известен (например, из
        :meth:`bridge_user_defined_launch_action` или :meth:`bridge_launch_action_info`),
        чтобы прочитать его настройки. Предусловий нет.

        Args:
            action_id: GUID действия запуска в строковом представлении. ``None``
                (по умолчанию) — параметр не передаётся.

        Returns:
            Данные действия как ``str``. Если сервер вернул ``null`` — пустая
            строка ``""``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                data = await ips.bridge_launch_action_data(
                    action_id="cad001c5-306c-11d8-b4e9-00304f19f545",
                )

        Notes:
            ``operationId``: ``Bridge_GetLaunchActionData``; путь
            ``GET /core/api/Bridge/Launch/GetLaunchActionData``. Ключ query —
            ``actionId``.
        """
        params: dict[str, Any] = {}
        if action_id is not None:
            params["actionId"] = action_id
        data = await self._request(
            "get", "/core/api/Bridge/Launch/GetLaunchActionData", params=params
        )
        return "" if data is None else str(data)
