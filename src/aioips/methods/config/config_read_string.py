"""Метод чтения строкового параметра конфигурации сервера IPS."""

from typing import Any

from ...core import APIManager


class ConfigReadStringMixin(APIManager):
    """Реализует метод ``GET /core/api/Config/ReadString`` (``Config_ReadString``)."""

    async def config_read_string(
        self: "ConfigReadStringMixin",
        *,
        module_name: str | None = None,
        section_id: int | None = None,
        param_name: str | None = None,
        default_value: str | None = None,
        config_mode: int | None = None,
    ) -> str:
        """Читает строковый параметр конфигурации сервера IPS.

        Возвращает значение одного параметра серверной конфигурации как строку.
        Параметр адресуется тройкой «модуль / секция / имя»: ``module_name`` задаёт
        подсистему-владельца настройки, ``section_id`` — числовую секцию внутри неё,
        ``param_name`` — конкретный ключ. Если параметр не найден, сервер возвращает
        ``default_value``. Базовый метод чтения текстовых настроек сервера; типизованные
        варианты — :meth:`config_read_bool`, :meth:`config_read_integer`,
        :meth:`config_read_double`, :meth:`config_read_date_time`. Кэширующий обход —
        :meth:`config_read_string_no_cache`.

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
            Значение параметра как ``str``. Если сервер вернул ``null`` — пустая
            строка ``""``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                vault = await ips.config_read_string(
                    module_name="Vault",
                    param_name="RootPath",
                )

        Notes:
            ``operationId``: ``Config_ReadString``; путь
            ``GET /core/api/Config/ReadString``. Ключ секции в query — ``sectionID``.
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
        data = await self._request("get", "/core/api/Config/ReadString", params=params)
        return "" if data is None else str(data)
