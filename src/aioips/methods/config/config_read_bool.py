"""Метод чтения булева параметра конфигурации сервера IPS."""

from typing import Any

from ...core import APIManager


class ConfigReadBoolMixin(APIManager):
    """Реализует метод ``GET /core/api/Config/ReadBool`` (``Config_ReadBool``)."""

    async def config_read_bool(
        self: "ConfigReadBoolMixin",
        *,
        module_name: str | None = None,
        section_id: int | None = None,
        param_name: str | None = None,
        default_value: str | None = None,
        config_mode: int | None = None,
    ) -> bool:
        """Читает булев параметр конфигурации сервера IPS.

        Возвращает значение одного параметра серверной конфигурации, приведённое к
        ``bool``. Параметр адресуется тройкой «модуль / секция / имя»: ``module_name``
        задаёт подсистему-владельца настройки, ``section_id`` — числовую секцию внутри
        неё, ``param_name`` — конкретный ключ. Если параметр не найден, сервер
        возвращает ``default_value`` (строковое значение по умолчанию, интерпретируемое
        как булево). Применяйте для чтения флагов-переключателей конфигурации сервера;
        для строковых/числовых настроек см. :meth:`config_read_string`,
        :meth:`config_read_integer`, :meth:`config_read_double`.

        Args:
            module_name: Имя модуля (подсистемы) — владельца параметра. ``None`` —
                не передавать (сервер применит свой контекст по умолчанию).
            section_id: Числовой идентификатор секции внутри модуля. ``None`` —
                не передавать.
            param_name: Имя читаемого параметра. ``None`` — не передавать.
            default_value: Значение по умолчанию (строкой), возвращаемое сервером,
                если параметр отсутствует. ``None`` — не передавать.
            config_mode: Режим конфигурации (числовой селектор источника настроек).
                ``None`` — не передавать.

        Returns:
            Значение параметра как ``bool``. Если сервер вернул пустой ответ —
            ``False``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                enabled = await ips.config_read_bool(
                    module_name="Core",
                    param_name="UseCache",
                    default_value="false",
                )

        Notes:
            ``operationId``: ``Config_ReadBool``; путь ``GET /core/api/Config/ReadBool``.
            Ключ секции в query — ``sectionID`` (акроним заглавный).
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
        data = await self._request("get", "/core/api/Config/ReadBool", params=params)
        return bool(data) if data is not None else False
