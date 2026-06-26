"""Метод получения доступных режимов отображения справочной системы IMBASE."""

from ...core import APIManager
from ...schemas.imbase import DisplayModeOption


class ImBaseDisplayModeOptionsMixin(APIManager):
    """Реализует ``GET /core/api/imbase/displayModeOptions`` (``ImBase_GetDisplayModeOptions``)."""

    async def imbase_display_mode_options(
        self: "ImBaseDisplayModeOptionsMixin",
    ) -> list[DisplayModeOption]:
        """Возвращает доступные режимы отображения каталогов/таблиц IMBASE.

        Справочная система IMBASE может отображать содержимое в нескольких режимах
        (общий, персональный, по роли). Метод отдаёт перечень доступных режимов с их
        названиями для интерфейса.

        Когда применять: для построения переключателя режимов отображения IMBASE на
        клиенте. Те же данные входят в сводный снимок
        :meth:`imbase_client_cache_state` (поле ``display_mode_options``).
        Предусловий нет (операция чтения).

        Returns:
            Список режимов по схеме :class:`DisplayModeOption` (поля ``mode`` и
            ``name``). Пустой список означает отсутствие доступных режимов.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                modes = await ips.imbase_display_mode_options()
                for option in modes:
                    print(option.mode, option.name)

        Notes:
            operationId ``ImBase_GetDisplayModeOptions``; путь
            ``GET /core/api/imbase/displayModeOptions`` (массив ``DisplayModeOptionDto``,
            без result-обёртки).
        """
        data = await self._request("get", "/core/api/imbase/displayModeOptions")
        return [DisplayModeOption.model_validate(item) for item in data]
