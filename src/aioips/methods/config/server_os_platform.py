"""Метод получения платформы ОС сервера IPS."""

from ...core import APIManager


class ServerOsPlatformMixin(APIManager):
    """Реализует ``GET /core/api/Config/GetServerOsPlatform`` (``Config_GetServerOsPlatform``)."""

    async def server_os_platform(self: "ServerOsPlatformMixin") -> str:
        """Возвращает платформу операционной системы, на которой работает сервер IPS.

        Отдаёт строковый идентификатор ОС серверной части (например, ``"Windows"`` или
        ``"Linux"``). Метод не принимает параметров и не зависит от тройки адресации
        конфигурации. Полезно для диагностики окружения и выбора платформозависимого
        поведения клиента (разделители путей, доступные функции). Прочие настройки
        сервера читаются типизованными методами раздела (см. :meth:`config_read_string`
        и др.).

        Returns:
            Платформа ОС сервера как ``str``. Если сервер вернул ``null`` — пустая
            строка ``""``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                platform = await ips.server_os_platform()
                print(platform)  # например, "Windows"

        Notes:
            ``operationId``: ``Config_GetServerOsPlatform``; путь
            ``GET /core/api/Config/GetServerOsPlatform`` (без параметров).
        """
        data = await self._request("get", "/core/api/Config/GetServerOsPlatform")
        return "" if data is None else str(data)
