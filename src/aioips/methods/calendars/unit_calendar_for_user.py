"""Метод получения календаря подразделения пользователя."""

from ...core import APIManager
from ...schemas.calendars import Calendar


class UnitCalendarForUserMixin(APIManager):
    """Реализует ``GET /core/api/calendars/unitCalendarForUser/{userId}``.

    operationId ``Calendars_GetUnitCalendarForUser``.
    """

    async def unit_calendar_for_user(self: "UnitCalendarForUserMixin", user_id: int) -> Calendar:
        """Возвращает календарь подразделения, к которому относится пользователь.

        Загружает производственный календарь организационного подразделения (а не
        личный календарь) указанного пользователя. Применяйте, когда планирование
        ведётся по календарю подразделения сотрудника. Для личного календаря
        пользователя используйте :meth:`user_calendar_settings`.

        Предусловие по id-пространству: аргумент — это идентификатор ПОЛЬЗОВАТЕЛЯ
        (``userId``), а не идентификатор календаря или подразделения. Сервер сам
        находит подразделение пользователя и возвращает его календарь.

        Args:
            user_id: Идентификатор пользователя (``userId``).

        Returns:
            Календарь подразделения пользователя по схеме :class:`Calendar`.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                cal = await ips.unit_calendar_for_user(42)
                print(cal.calendar_id, cal.owner)

        Notes:
            operationId ``Calendars_GetUnitCalendarForUser``; путь
            ``GET /core/api/calendars/unitCalendarForUser/{userId}`` (``CalendarContract``).
        """
        data = await self._request("get", f"/core/api/calendars/unitCalendarForUser/{user_id}")
        return Calendar.model_validate(data)
