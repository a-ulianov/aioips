"""Тесты методов чтения раздела календарей.

``CalendarsAPI`` ещё не подключён к :class:`aioips.IPSClient` (это потребовало бы
правки ``client.py`` вне рамок задачи). Так как каждый mixin наследует
:class:`aioips.core.APIManager` (конструктор, контекст-менеджер, ``_request``),
здесь поднимается локальный клиент ``CalendarsClient`` — прямой наследник
``CalendarsAPI`` — и проверяется через него.
"""

from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.methods.calendars import CalendarsAPI


class CalendarsClient(CalendarsAPI):
    """Минимальный клиент только с методами календарей для изоляции тестов."""


_CALENDAR = {
    "calendarId": 7,
    "name": "Производственный 2024",
    "caption": "Производственный календарь",
    "owner": "calendarObject",
    "weekStartDay": "monday",
    "yearStartMonth": "january",
    "daysInMonth": 21,
    "hoursInDay": 8.0,
    "hoursInWeek": 40.0,
    "defaultStartHour": 9,
    "defaultStartMinute": 0,
    "defaultFinishHour": 18,
    "defaultFinishMinute": 0,
    "whereIsFromAdditionalCalendar": "standardCalendar",
    "additionalCalendar": None,
    "standardWeek": {"weekDays": []},
    "standardWorkPeriods": [
        {"startHours": 9, "startMinutes": 0, "finishHours": 18, "finishMinutes": 0}
    ],
    "specialCalendarDays": None,
    "unitId": 11,
    "userId": 42,
}


async def test_calendars_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    body = [
        {"calendarId": 7, "name": "Производственный 2024"},
        {"calendarId": 8, "name": "Сменный график"},
    ]
    fake_ips.add("get", "/core/api/calendars", body=body)
    async with CalendarsClient(config=token_config) as ips:
        calendars = await ips.calendars()

    assert len(calendars) == 2
    assert calendars[0].calendar_id == 7
    assert calendars[0].name == "Производственный 2024"
    assert calendars[1].calendar_id == 8


async def test_calendar_settings_parses_contract(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/calendars/calendarSettings/7", body=_CALENDAR)
    async with CalendarsClient(config=token_config) as ips:
        cal = await ips.calendar_settings(7)

    assert cal.calendar_id == 7
    assert cal.name == "Производственный 2024"
    assert cal.owner == "calendarObject"
    assert cal.week_start_day == "monday"
    assert cal.year_start_month == "january"
    assert cal.hours_in_week == 40.0
    assert cal.default_finish_hour == 18
    assert cal.where_is_from_additional_calendar == "standardCalendar"
    assert cal.unit_id == 11
    assert cal.user_id == 42
    assert cal.additional_calendar is None
    assert cal.standard_week == {"weekDays": []}
    assert len(cal.standard_work_periods) == 1
    # specialCalendarDays пришёл null -> приведён к пустому списку (EmptyListIfNone)
    assert cal.special_calendar_days == []


async def test_unit_calendar_for_user(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/calendars/unitCalendarForUser/42", body=_CALENDAR)
    async with CalendarsClient(config=token_config) as ips:
        cal = await ips.unit_calendar_for_user(42)

    assert cal.calendar_id == 7
    assert cal.owner == "calendarObject"


async def test_user_calendar_settings(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/calendars/userCalendarSettings/42", body=_CALENDAR)
    async with CalendarsClient(config=token_config) as ips:
        cal = await ips.user_calendar_settings(42)

    assert cal.calendar_id == 7
    assert cal.user_id == 42
