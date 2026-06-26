"""Метод чтения целочисленного параметра конфигурации сервера IPS."""

from typing import Any

from ...core import APIManager


class ConfigReadIntegerMixin(APIManager):
    """Реализует метод ``GET /core/api/Config/ReadInteger`` (``Config_ReadInteger``)."""

    async def config_read_integer(
        self: "ConfigReadIntegerMixin",
        *,
        module_name: str | None = None,
        section_id: int | None = None,
        param_name: str | None = None,
        default_value: str | None = None,
        config_mode: int | None = None,
    ) -> int:
        """Читает целочисленный параметр конфигурации сервера IPS.

        Возвращает значение одного параметра серверной конфигурации, приведённое к
        ``int``. Параметр адресуется тройкой «модуль / секция / имя»: ``module_name``
        задаёт подсистему-владельца настройки, ``section_id`` — числовую секцию внутри
        неё, ``param_name`` — конкретный ключ. Если параметр не найден, сервер
        возвращает ``default_value`` (строкой, интерпретируемое как целое). Применяйте
        для числовых настроек (счётчики, лимиты, порты); для дробных см.
        :meth:`config_read_double`, для строк — :meth:`config_read_string`.

        Args:
            module_name: Имя модуля (подсистемы) — владельца параметра. ``None`` —
                не передавать.
            section_id: Числовой идентификатор секции внутри модуля. ``None`` —
                не передавать.
            param_name: Имя читаемого параметра. ``None`` — не передавать.
            default_value: Значение по умолчанию (строкой), возвращаемое сервером,
                если параметр отсутствует. ``None`` — не передавать.
            config_mode: Режим конфигурации (числовой селектор источника настроек).
                ``None`` — не передавать.

        Returns:
            Значение параметра как ``int``. Если сервер вернул пустой ответ — ``0``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                limit = await ips.config_read_integer(
                    module_name="Core",
                    param_name="MaxConnections",
                    default_value="100",
                )

        Notes:
            ``operationId``: ``Config_ReadInteger``; путь
            ``GET /core/api/Config/ReadInteger``. Ключ секции в query — ``sectionID``.
        """
        params: dict[str, Any] = {}
        if module_name is not None:
            params["moduleName"] = module_name
        if section_id is not None:
            params["sectionID"] = section_id
        if param_name is not None:
            params["paramName"] = param_name
        if default_value is not None:
            params["defaultValue"] = default_value
        if config_mode is not None:
            params["configMode"] = config_mode
        data = await self._request("get", "/core/api/Config/ReadInteger", params=params)
        return int(data) if data is not None else 0
