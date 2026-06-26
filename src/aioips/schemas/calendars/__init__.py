"""Схемы раздела календарей IPS Web API."""

from .calendar import Calendar
from .calendar_name import CalendarName
from .filter_contract import CalendarFilter

__all__ = ["Calendar", "CalendarFilter", "CalendarName"]
