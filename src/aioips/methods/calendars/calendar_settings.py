"""Метод загрузки настроек календаря по идентификатору."""

from ...core import APIManager
from ...schemas.calendars import Calendar


class CalendarSettingsMixin(APIManager):
    """Реализует ``GET /core/api/calendars/calendarSettings/{calendarId}``.

    operationId ``Calendars_LoadCalendarSettings``.
    """

    async def calendar_settings(self: "CalendarSettingsMixin", calendar_id: int) -> Calendar:
        """Возвращает полные настройки календаря по его идентификатору.

        Загружает производственный календарь целиком: владельца, параметры недели/года,
        длительности рабочего дня/недели, стандартную неделю, рабочие периоды и особые
        дни. Применяйте после выбора календаря из :meth:`calendars`, когда нужны не имя,
        а сами параметры (например, для расчёта рабочего времени).

        Предусловие по id-пространству: аргумент — это ``calendarId`` (идентификатор
        календаря из :meth:`calendars`), а не идентификатор пользователя/подразделения.
        Для календаря пользователя см. :meth:`user_calendar_settings`, для календаря
        подразделения пользователя — :meth:`unit_calendar_for_user`.

        Args:
            calendar_id: Идентификатор календаря (``calendarId``).

        Returns:
            Настройки календаря по схеме :class:`Calendar`.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если календаря нет).

        Example:
            async with IPSClient(config=config) as ips:
                cal = await ips.calendar_settings(7)
                print(cal.name, cal.hours_in_week)

        Notes:
            operationId ``Calendars_LoadCalendarSettings``; путь
            ``GET /core/api/calendars/calendarSettings/{calendarId}`` (``CalendarContract``).
        """
        data = await self._request("get", f"/core/api/calendars/calendarSettings/{calendar_id}")
        return Calendar.model_validate(data)
