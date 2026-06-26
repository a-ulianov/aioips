"""Метод обновления настроек действия запуска IPS Bridge (мутация)."""

from typing import Any

from ...core import APIManager


class BridgeUpdateLaunchActionMixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Launch/UpdateLaunchAction``.

    ``operationId``: ``Bridge_UpdateLaunchAction``.
    """

    async def bridge_update_launch_action(
        self: "BridgeUpdateLaunchActionMixin",
        settings_xml: str,
        *,
        action_id: str | None = None,
        confirm: bool = False,
    ) -> None:
        """Обновляет XML-настройки действия запуска IPS Bridge (МУТАЦИЯ).

        IPS Bridge — серверный помощник десктоп-клиента; действие запуска
        (launch action) описывает операцию над объектом на стороне клиента.
        Метод перезаписывает настройки существующего действия (тело — строка
        XML) по его GUID. Создать действие — :meth:`bridge_create_launch_action`.

        Обратимость: операция ОБРАТИМА по схеме write-same-back — сохраните
        прежние настройки (например, из :meth:`bridge_launch_action_data`) и для
        отката запишите их обратно тем же методом.

        Защита: меняет настройки на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            settings_xml: Новые XML-настройки действия (тело запроса, строка).
            action_id: GUID обновляемого действия. ``None`` — параметр не
                передаётся.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие
            ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (404, если действие не найдено).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.bridge_update_launch_action(
                    "<settings/>",
                    action_id="cad001c5-306c-11d8-b4e9-00304f19f545",
                    confirm=True,
                )

        Notes:
            ``operationId``: ``Bridge_UpdateLaunchAction``; путь
            ``POST /core/api/Bridge/Launch/UpdateLaunchAction``. Ключ query —
            ``actionId``; тело — сырая строка (``string``).
        """
        if confirm is not True:
            raise ValueError(
                "bridge_update_launch_action меняет настройки действия; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if action_id is not None:
            params["actionId"] = action_id
        # Эндпоинт ждёт JSON-строку в теле; ``JsonBody`` строку не моделирует,
        # поэтому приводим к ``Any`` (aiohttp сериализует строку как JSON-строку).
        await self._request(
            "post",
            "/core/api/Bridge/Launch/UpdateLaunchAction",
            params=params,
            json=settings_xml,
        )
        return None
