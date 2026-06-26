"""Метод чтения строкового параметра конфигурации в обход кэша."""

from typing import Any

from ...core import APIManager


class ConfigReadStringNoCacheMixin(APIManager):
    """Реализует ``GET /core/api/Config/ReadStringNoCache`` (``Config_ReadStringNoCache``)."""

    async def config_read_string_no_cache(
        self: "ConfigReadStringNoCacheMixin",
        *,
        module_name: str | None = None,
        section_id: int | None = None,
        param_name: str | None = None,
        is_global_param: bool | None = None,
    ) -> str:
        """Читает строковый параметр конфигурации сервера IPS в обход кэша.

        Возвращает актуальное значение строкового параметра напрямую из хранилища
        конфигурации, минуя серверный кэш. Применяйте, когда нужно гарантированно
        свежее значение (например, после внешнего изменения настройки), тогда как
        обычное кэширующее чтение даёт :meth:`config_read_string`. Параметр адресуется
        тройкой «модуль / секция / имя»; флаг ``is_global_param`` уточняет область
        видимости (глобальный параметр против локального).

        Args:
            module_name: Имя модуля (подсистемы) — владельца параметра. ``None`` —
                не передавать.
            section_id: Числовой идентификатор секции внутри модуля. ``None`` —
                не передавать.
            param_name: Имя читаемого параметра. ``None`` — не передавать.
            is_global_param: ``True`` — читать как глобальный параметр, ``False`` —
                как локальный. В query сериализуется как ``"true"``/``"false"``.
                ``None`` — не передавать.

        Returns:
            Значение параметра как ``str``. Если сервер вернул ``null`` — пустая
            строка ``""``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                fresh = await ips.config_read_string_no_cache(
                    module_name="Vault",
                    param_name="RootPath",
                    is_global_param=True,
                )

        Notes:
            ``operationId``: ``Config_ReadStringNoCache``; путь
            ``GET /core/api/Config/ReadStringNoCache``. Ключ секции в query —
            ``sectionID``; булев флаг — ``isGlobalParam``.
        """
        params: dict[str, Any] = {}
        if module_name is not None:
            params["moduleName"] = module_name
        if section_id is not None:
            params["sectionID"] = section_id
        if param_name is not None:
            params["paramName"] = param_name
        if is_global_param is not None:
            params["isGlobalParam"] = str(is_global_param).lower()
        data = await self._request("get", "/core/api/Config/ReadStringNoCache", params=params)
        return "" if data is None else str(data)
