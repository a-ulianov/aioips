"""Метод загрузки пользовательского фильтра календарей."""

from ...core import APIManager
from ...schemas.calendars import CalendarFilter


class UserCalendarFilterMixin(APIManager):
    """Реализует ``GET /core/api/calendars/userFilter``.

    operationId ``Calendars_LoadUserCalendarFilter``.
    """

    async def user_calendar_filter(self: "UserCalendarFilterMixin") -> CalendarFilter:
        """Возвращает персональный фильтр особых дней календаря текущего пользователя.

        Загружает критерии отбора особых дней (диапазон дат, типы периодов, типы
        дней, причина), сохранённые лично текущим пользователем (определяется по
        токену авторизации). Применяйте, чтобы воспроизвести индивидуальные настройки
        фильтрации сотрудника при просмотре особых дней календаря (см. :class:`Calendar`,
        поле ``special_calendar_days``). Для общесистемного фильтра по умолчанию
        используйте :meth:`base_calendar_filter`.

        Параметров нет: пользователь берётся из контекста авторизации, а не из
        аргумента. В каждом критерии есть парный флаг ``use_*`` — критерий учитывается,
        только если флаг ``True``.

        Returns:
            Персональный фильтр текущего пользователя по схеме :class:`CalendarFilter`.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                flt = await ips.user_calendar_filter()
                if flt.use_start_date_time:
                    print(flt.start_date_time, flt.finish_date_time)

        Notes:
            operationId ``Calendars_LoadUserCalendarFilter``; путь
            ``GET /core/api/calendars/userFilter`` (``FilterContract``). Парный
            общесистемному :meth:`base_calendar_filter`; связан с :meth:`calendars`.
        """
        data = await self._request("get", "/core/api/calendars/userFilter")
        return CalendarFilter.model_validate(data)
