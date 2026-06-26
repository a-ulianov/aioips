"""Метод чтения XML-настроек интегратора IPS Bridge."""

from typing import Any

from ...core import APIManager


class BridgeSettingsXmlMixin(APIManager):
    """Реализует ``GET /core/api/Bridge/Integrators/GetSettingsXml`` (``Bridge_GetSettingsXml``)."""

    async def bridge_settings_xml(
        self: "BridgeSettingsXmlMixin",
        *,
        integrator_guid: str | None = None,
    ) -> str:
        """Возвращает XML-настройки интегратора IPS Bridge.

        Интеграторы IPS Bridge — клиентские компоненты интеграции с внешними
        приложениями; их конфигурация хранится в виде XML. Метод отдаёт этот XML
        как строку. Применяйте, чтобы прочитать настройки конкретного интегратора
        (по его GUID) или общие настройки, если GUID не задан. Предусловий нет.

        Args:
            integrator_guid: GUID интегратора в строковом представлении. Если
                ``None`` (по умолчанию), параметр не передаётся и сервер вернёт
                настройки по умолчанию.

        Returns:
            XML-настройки как ``str``. Если сервер вернул ``null`` — пустая
            строка ``""``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                xml = await ips.bridge_settings_xml(
                    integrator_guid="cad001c5-306c-11d8-b4e9-00304f19f545",
                )

        Notes:
            ``operationId``: ``Bridge_GetSettingsXml``; путь
            ``GET /core/api/Bridge/Integrators/GetSettingsXml``. Ключ query —
            ``integratorGuid``.
        """
        params: dict[str, Any] = {}
        if integrator_guid is not None:
            params["integratorGuid"] = integrator_guid
        data = await self._request(
            "get", "/core/api/Bridge/Integrators/GetSettingsXml", params=params
        )
        return "" if data is None else str(data)
