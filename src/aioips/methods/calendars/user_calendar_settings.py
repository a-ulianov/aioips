"""Метод загрузки личного календаря пользователя."""

from ...core import APIManager
from ...schemas.calendars import Calendar


class UserCalendarSettingsMixin(APIManager):
    """Реализует ``GET /core/api/calendars/userCalendarSettings/{userId}``.

    operationId ``Calendars_LoadUserCalendarSettings``.
    """

    async def user_calendar_settings(self: "UserCalendarSettingsMixin", user_id: int) -> Calendar:
        """Возвращает личный (пользовательский) календарь по идентификатору пользователя.

        Загружает производственный календарь, привязанный лично к пользователю
        (``owner = user``), со всеми настройками. Применяйте, когда планирование ведётся
        по индивидуальному календарю сотрудника. Для календаря подразделения сотрудника
        используйте :meth:`unit_calendar_for_user`, для произвольного календаря по его
        идентификатору — :meth:`calendar_settings`.

        Предусловие по id-пространству: аргумент — это идентификатор ПОЛЬЗОВАТЕЛЯ
        (``userId``), а не идентификатор календаря.

        Args:
            user_id: Идентификатор пользователя (``userId``).

        Returns:
            Личный календарь пользователя по схеме :class:`Calendar`.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                cal = await ips.user_calendar_settings(42)
                print(cal.user_id, cal.hours_in_day)

        Notes:
            operationId ``Calendars_LoadUserCalendarSettings``; путь
            ``GET /core/api/calendars/userCalendarSettings/{userId}`` (``CalendarContract``).
        """
        data = await self._request("get", f"/core/api/calendars/userCalendarSettings/{user_id}")
        return Calendar.model_validate(data)
