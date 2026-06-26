"""Метод чтения параметра-даты конфигурации сервера IPS."""

from typing import Any

from ...core import APIManager


class ConfigReadDateTimeMixin(APIManager):
    """Реализует метод ``GET /core/api/Config/ReadDateTime`` (``Config_ReadDateTime``)."""

    async def config_read_date_time(
        self: "ConfigReadDateTimeMixin",
        *,
        module_name: str | None = None,
        section_id: int | None = None,
        param_name: str | None = None,
        default_value: str | None = None,
        config_mode: int | None = None,
    ) -> str:
        """Читает параметр-дату/время конфигурации сервера IPS.

        Возвращает значение одного параметра серверной конфигурации, хранящего
        дату/время, в виде ISO-строки (как отдаёт сервер; разбор в ``datetime`` —
        на стороне вызывающего). Параметр адресуется тройкой «модуль / секция / имя»:
        ``module_name`` задаёт подсистему-владельца настройки, ``section_id`` — числовую
        секцию внутри неё, ``param_name`` — конкретный ключ. Если параметр не найден,
        сервер возвращает ``default_value``. Применяйте для настроек-меток времени;
        для прочих типов см. :meth:`config_read_string`, :meth:`config_read_integer`,
        :meth:`config_read_double`, :meth:`config_read_bool`.

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
            Значение параметра как ISO-строка ``str`` (например,
            ``"2026-06-24T00:00:00"``). Если сервер вернул ``null`` — пустая строка
            ``""``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                raw = await ips.config_read_date_time(
                    module_name="Core",
                    param_name="LastSync",
                )
                # при необходимости: datetime.fromisoformat(raw)

        Notes:
            ``operationId``: ``Config_ReadDateTime``; путь
            ``GET /core/api/Config/ReadDateTime``. Ключ секции в query — ``sectionID``.
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
        data = await self._request("get", "/core/api/Config/ReadDateTime", params=params)
        return "" if data is None else str(data)
