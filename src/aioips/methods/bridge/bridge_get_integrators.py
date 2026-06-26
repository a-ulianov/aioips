"""Метод получения карты интеграторов IPS Bridge."""

from typing import Any

from ...core import APIManager


class BridgeGetIntegratorsMixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Integrators/GetIntegrators``.

    ``operationId``: ``Bridge_GetIntegrators``.
    """

    async def bridge_get_integrators(
        self: "BridgeGetIntegratorsMixin",
    ) -> dict[str, Any]:
        """Возвращает карту интеграторов, зарегистрированных в IPS Bridge.

        IPS Bridge — серверный помощник десктоп-клиента; интеграторы — это
        клиентские компоненты связи с внешними приложениями. Метод отдаёт их
        как словарь (структура задаётся сервером: обычно сопоставление
        GUID интегратора → его описание/настройки). Это операция ЧТЕНИЯ —
        подтверждения не требует. XML-настройки конкретного интегратора
        читаются через :meth:`bridge_settings_xml`, удаление —
        :meth:`bridge_remove_integrator`. Предусловий нет.

        Returns:
            ``dict`` с интеграторами (произвольная структура от сервера). Если
            сервер вернул ``null`` — пустой словарь ``{}``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                integrators = await ips.bridge_get_integrators()

        Notes:
            ``operationId``: ``Bridge_GetIntegrators``; путь
            ``POST /core/api/Bridge/Integrators/GetIntegrators``. Тело не
            передаётся (отправляется ``{}`` во избежание ошибки 415).
        """
        data = await self._request("post", "/core/api/Bridge/Integrators/GetIntegrators", json={})
        return {} if data is None else dict(data)
