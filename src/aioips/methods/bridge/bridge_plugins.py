"""Метод получения списка плагинов IPS Bridge."""

from ...core import APIManager
from ...schemas.bridge import PluginInfo


class BridgePluginsMixin(APIManager):
    """Реализует ``GET /core/api/Bridge/GetPlugins`` (``Bridge_GetPlugins``)."""

    async def bridge_plugins(self: "BridgePluginsMixin") -> list[PluginInfo]:
        """Возвращает список клиентских плагинов, зарегистрированных в IPS Bridge.

        Плагины расширяют функциональность клиента IPS через мост. Метод отдаёт
        перечень зарегистрированных плагинов с их объектными идентификаторами,
        именами и сведениями о сборках. Применяйте для диагностики состава и
        версий клиентских расширений (например, проверки совместимости).
        Предусловий нет.

        Returns:
            Список плагинов по схеме :class:`PluginInfo`. Пустой список означает,
            что плагины не зарегистрированы.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                plugins = await ips.bridge_plugins()
                for plugin in plugins:
                    print(plugin.plugin_name, plugin.assembly_version)

        Notes:
            ``operationId``: ``Bridge_GetPlugins``; путь
            ``GET /core/api/Bridge/GetPlugins`` (голый массив ``PluginInfoDTO``).
        """
        data = await self._request("get", "/core/api/Bridge/GetPlugins")
        return [PluginInfo.model_validate(item) for item in data]
