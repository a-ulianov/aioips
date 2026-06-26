"""Метод загрузки базового фильтра календарей."""

from ...core import APIManager
from ...schemas.calendars import CalendarFilter


class BaseCalendarFilterMixin(APIManager):
    """Реализует ``GET /core/api/calendars/baseFilter``.

    operationId ``Calendars_LoadBaseCalendarFilter``.
    """

    async def base_calendar_filter(self: "BaseCalendarFilterMixin") -> CalendarFilter:
        """Возвращает базовый (общесистемный) фильтр особых дней календаря.

        Загружает критерии отбора особых дней (диапазон дат, типы периодов, типы
        дней, причина) уровня системы — без привязки к конкретному пользователю.
        Применяйте, чтобы узнать настройки фильтрации по умолчанию перед просмотром
        особых дней календаря (см. :class:`Calendar`, поле ``special_calendar_days``).
        Для персонального фильтра текущего пользователя используйте
        :meth:`user_calendar_filter`.

        Параметров нет: фильтр относится к системе целиком. В каждом критерии есть
        парный флаг ``use_*`` — критерий учитывается, только если флаг ``True``.

        Returns:
            Базовый фильтр по схеме :class:`CalendarFilter`.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                flt = await ips.base_calendar_filter()
                if flt.use_special_day_types:
                    print(flt.special_day_types)

        Notes:
            operationId ``Calendars_LoadBaseCalendarFilter``; путь
            ``GET /core/api/calendars/baseFilter`` (``FilterContract``). Связан с
            :meth:`calendars` и :meth:`calendar_settings` (просмотр особых дней).
        """
        data = await self._request("get", "/core/api/calendars/baseFilter")
        return CalendarFilter.model_validate(data)
