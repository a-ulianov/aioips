"""Метод получения пользовательских параметров справочной системы IMBASE."""

from typing import Any

from ...core import APIManager


class ImBaseUserParamsMixin(APIManager):
    """Реализует ``GET /core/api/imbase/params/user`` (``ImBase_GetUserParams``)."""

    async def imbase_user_params(self: "ImBaseUserParamsMixin") -> dict[str, Any]:
        """Возвращает основные ПОЛЬЗОВАТЕЛЬСКИЕ (персональные) параметры IMBASE.

        Отдаёт персональные настройки отображения таблиц IMBASE текущего пользователя:
        скрывать пустые колонки, замораживать первую колонку, сохранять положение
        колонок/фильтр/пользовательский фильтр, а также назначенные цвета записей по
        значению атрибута «Применяемость».

        Когда применять: чтобы прочитать персональные настройки IMBASE текущего
        пользователя (например, для восстановления состояния таблиц). Эти же данные
        входят в сводный снимок :meth:`imbase_client_cache_state` (поле
        ``user_params``). Общесистемные параметры — :meth:`imbase_common_params`.

        Returns:
            Словарь параметров «как есть» (``dict[str, Any]``). Ключи в оригинальном
            ``camelCase`` API: ``hideEmptyColumns``, ``freezeFirstColumn``,
            ``saveColumnsState``, ``saveFilterState``, ``saveUserFilterState``,
            ``tableRecordsApplicabilityColors`` (вложенный словарь цветов). Если сервер
            вернул не объект — пустой словарь.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                params = await ips.imbase_user_params()
                print(params.get("hideEmptyColumns"))

        Notes:
            operationId ``ImBase_GetUserParams``; путь
            ``GET /core/api/imbase/params/user``. DTO ``MainImBaseUserParamsDto`` не
            типизируется схемой (повреждённый кириллический ключ в swagger), поэтому
            ответ возвращается как «сырой» словарь.
        """
        data = await self._request("get", "/core/api/imbase/params/user")
        return data if isinstance(data, dict) else {}
