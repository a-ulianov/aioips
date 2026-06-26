"""Метод получения состояния клиентского кэша справочной системы IMBASE."""

from ...core import APIManager
from ...schemas.imbase import ImBaseClientCacheState


class ImBaseClientCacheStateMixin(APIManager):
    """Реализует ``GET /core/api/imbase/clientCacheState`` (``ImBase_GetClientCacheState``)."""

    async def imbase_client_cache_state(
        self: "ImBaseClientCacheStateMixin",
    ) -> ImBaseClientCacheState:
        """Возвращает сводное состояние клиентского кэша справочной системы IMBASE.

        Один агрегированный снимок параметров и метаданных IMBASE для инициализации
        клиента без серии отдельных запросов: режимы отображения, ролевые режимы,
        общие и пользовательские параметры, терминальные папки и информация об индексах.

        Когда применять: при старте клиента IMBASE для разовой загрузки всего состояния.
        Отдельные части доступны точечно: режимы — :meth:`imbase_display_mode_options`,
        индексы — :meth:`imbase_indexes`. Предусловий нет (операция чтения).

        Returns:
            Состояние кэша по схеме :class:`ImBaseClientCacheState`. Значимые поля:
            ``display_mode_options`` (режимы), ``terminal_folder_ids`` (конечные папки),
            ``indexes_info`` (каталоги и индексы); ``common_params``/``user_params``/
            ``role_display_mode_options`` отдаются как сырые DTO (см. схему).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                state = await ips.imbase_client_cache_state()
                print(len(state.terminal_folder_ids), len(state.display_mode_options))

        Notes:
            operationId ``ImBase_GetClientCacheState``; путь
            ``GET /core/api/imbase/clientCacheState``. Ответ — прямой
            ``ImBaseClientCacheStateDto`` (без result-обёртки).
        """
        data = await self._request("get", "/core/api/imbase/clientCacheState")
        return ImBaseClientCacheState.model_validate(data)
