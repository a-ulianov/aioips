"""Метод получения списка календарей."""

from ...core import APIManager
from ...schemas.calendars import CalendarName


class CalendarsMixin(APIManager):
    """Реализует метод ``GET /core/api/calendars`` (``Calendars_GetAllCalendars``)."""

    async def calendars(self: "CalendarsMixin") -> list[CalendarName]:
        """Возвращает список всех календарей IPS (id + имя).

        Облегчённый справочник производственных календарей: каждый элемент содержит
        только идентификатор и имя. Применяйте, чтобы показать выбор календаря или
        найти ``calendar_id`` по имени; полные настройки выбранного календаря затем
        загружаются методом :meth:`calendar_settings`. Предусловий нет.

        Returns:
            Список календарей по схеме :class:`CalendarName`. Пустой список означает,
            что в базе не определено ни одного календаря.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                for cal in await ips.calendars():
                    print(cal.calendar_id, cal.name)

        Notes:
            operationId ``Calendars_GetAllCalendars``; путь
            ``GET /core/api/calendars`` (массив ``CalendarName``).
        """
        data = await self._request("get", "/core/api/calendars")
        return [CalendarName.model_validate(item) for item in data]
