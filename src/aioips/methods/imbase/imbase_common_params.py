"""Метод получения основных общих параметров справочной системы IMBASE."""

from typing import Any

from ...core import APIManager


class ImBaseCommonParamsMixin(APIManager):
    """Реализует ``GET /core/api/imbase/params/common`` (``ImBase_GetCommonParams``)."""

    async def imbase_common_params(self: "ImBaseCommonParamsMixin") -> dict[str, Any]:
        """Возвращает основные ОБЩИЕ (системные) параметры IMBASE.

        Отдаёт настройки справочной системы IMBASE уровня сервера (общие для всех
        пользователей): режим удаления записей, учёт прав видимости скрытых записей,
        расширенная проверка прав для индексов, запрет нескольких ярлыков на одну
        таблицу, учёт применяемости при формировании состава.

        Когда применять: чтобы прочитать общесистемную конфигурацию IMBASE. Эти же
        данные входят в сводный снимок :meth:`imbase_client_cache_state` (поле
        ``common_params``). Пользовательские (персональные) параметры — отдельный метод
        :meth:`imbase_user_params`.

        Returns:
            Словарь параметров «как есть» (``dict[str, Any]``). Ключи в оригинальном
            ``camelCase`` API: ``deleteRecordMode`` (``disable``/``ask``/``enable``),
            ``denyFewLinksForSameTable``, ``useExtendedSecurityCheckForIndexes``,
            ``checkApplicabilityBeforeCreateComposition`` и др. Если сервер вернул не
            объект — пустой словарь.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                params = await ips.imbase_common_params()
                print(params.get("deleteRecordMode"))

        Notes:
            operationId ``ImBase_GetCommonParams``; путь
            ``GET /core/api/imbase/params/common``. DTO ``MainImBaseCommonParamsDto``
            не типизируется схемой: в swagger имя одного из его полей содержит
            кириллический символ (повреждённый ключ), поэтому ответ возвращается как
            «сырой» словарь.
        """
        data = await self._request("get", "/core/api/imbase/params/common")
        return data if isinstance(data, dict) else {}
