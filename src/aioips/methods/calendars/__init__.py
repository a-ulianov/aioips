"""Методы раздела календарей IPS Web API."""

from .base_calendar_filter import BaseCalendarFilterMixin
from .calendar_settings import CalendarSettingsMixin
from .calendars import CalendarsMixin
from .set_base_calendar import SetBaseCalendarMixin
from .unit_calendar_for_user import UnitCalendarForUserMixin
from .unit_calendar_settings import UnitCalendarSettingsMixin
from .update_calendar_settings import UpdateCalendarSettingsMixin
from .update_user_calendar_settings import UpdateUserCalendarSettingsMixin
from .user_calendar_filter import UserCalendarFilterMixin
from .user_calendar_settings import UserCalendarSettingsMixin


class CalendarsAPI(
    CalendarsMixin,
    CalendarSettingsMixin,
    UnitCalendarForUserMixin,
    UserCalendarSettingsMixin,
    BaseCalendarFilterMixin,
    UserCalendarFilterMixin,
    UnitCalendarSettingsMixin,
    UpdateCalendarSettingsMixin,
    UpdateUserCalendarSettingsMixin,
    SetBaseCalendarMixin,
):
    """Объединяет методы раздела календарей.

    References:
        Эндпоинты ``/core/api/calendars/*`` IPS Server Web API.
    """


__all__ = ["CalendarsAPI"]
