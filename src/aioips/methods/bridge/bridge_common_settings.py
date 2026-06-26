"""Метод чтения общих настроек IPS Bridge."""

from ...core import APIManager
from ...schemas.bridge import CommonBridgeSettings


class BridgeCommonSettingsMixin(APIManager):
    """Реализует ``GET /core/api/Bridge/commonSettings`` (``Bridge_GetCommonSettings``)."""

    async def bridge_common_settings(
        self: "BridgeCommonSettingsMixin",
    ) -> CommonBridgeSettings:
        """Возвращает общие настройки клиентского моста IPS Bridge.

        IPS Bridge — локальный мост между толстым клиентом IPS и сервером. Метод
        отдаёт его общие параметры подключения (в частности, порт). Применяйте,
        чтобы узнать, на каком порту мост принимает локальные подключения, прежде
        чем обращаться к нему за пользователем, плагинами или действиями запуска.
        Предусловий нет.

        Returns:
            Настройки по схеме :class:`CommonBridgeSettings`. Поле
            ``ips_bridge_port`` равно ``0``, если порт не задан.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                settings = await ips.bridge_common_settings()
                print(settings.ips_bridge_port)

        Notes:
            ``operationId``: ``Bridge_GetCommonSettings``; путь
            ``GET /core/api/Bridge/commonSettings``.
        """
        data = await self._request("get", "/core/api/Bridge/commonSettings")
        return CommonBridgeSettings.model_validate(data)
