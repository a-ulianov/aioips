"""Тесты дополнительных read-методов раздела календарей.

Проверяются ``base_calendar_filter`` / ``user_calendar_filter`` (``FilterContract``)
и ``unit_calendar_settings`` (``CalendarContract``). Как и в ``test_calendars_read``,
поднимается локальный клиент ``CalendarsClient`` — прямой наследник ``CalendarsAPI``,
так как раздел ещё не подключён к :class:`aioips.IPSClient`.
"""

from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.methods.calendars import CalendarsAPI
from aioips.methods.calendars.base_calendar_filter import BaseCalendarFilterMixin
from aioips.methods.calendars.unit_calendar_settings import UnitCalendarSettingsMixin
from aioips.methods.calendars.user_calendar_filter import UserCalendarFilterMixin


class CalendarsClient(
    CalendarsAPI,
    BaseCalendarFilterMixin,
    UserCalendarFilterMixin,
    UnitCalendarSettingsMixin,
):
    """Минимальный клиент только с методами календарей для изоляции тестов.

    Новые mixin'ы подмешаны явно: ``CalendarsAPI.__init__`` ещё не обновлён (правка
    ``methods/calendars/__init__.py`` вне рамок задачи), поэтому тест собирает
    клиент из нужных mixin'ов напрямую.
    """


# Точные ключи FilterContract (camelCase) из swagger.
_FILTER = {
    "startDateTime": "2024-01-01T00:00:00Z",
    "finishDateTime": "2024-12-31T00:00:00Z",
    "typeSpecialDayPeriods": ["vacation", "businessTrip"],
    "specialDayTypes": None,
    "reason": "перенос",
    "useStartDateTime": True,
    "useFinishDateTime": True,
    "useTypeSpecialDayPeriods": True,
    "useSpecialDayTypes": False,
    "useReason": True,
}

_UNIT_CALENDAR = {
    "calendarId": 9,
    "name": "Календарь подразделения",
    "owner": "organizationUnit",
    "weekStartDay": "monday",
    "yearStartMonth": "january",
    "unitId": 11,
    "additionalCalendar": None,
    "standardWeek": {"weekDays": []},
    "standardWorkPeriods": None,
    "specialCalendarDays": None,
}


async def test_base_calendar_filter_parses_contract(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/calendars/baseFilter", body=_FILTER)
    async with CalendarsClient(config=token_config) as ips:
        flt = await ips.base_calendar_filter()

    assert flt.start_date_time == "2024-01-01T00:00:00Z"
    assert flt.finish_date_time == "2024-12-31T00:00:00Z"
    assert flt.type_special_day_periods == ["vacation", "businessTrip"]
    assert flt.reason == "перенос"
    assert flt.use_start_date_time is True
    assert flt.use_special_day_types is False
    # specialDayTypes пришёл null -> приведён к пустому списку (EmptyListIfNone)
    assert flt.special_day_types == []


async def test_user_calendar_filter_parses_contract(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/calendars/userFilter", body=_FILTER)
    async with CalendarsClient(config=token_config) as ips:
        flt = await ips.user_calendar_filter()

    assert flt.use_finish_date_time is True
    assert flt.use_type_special_day_periods is True
    assert flt.use_reason is True
    assert flt.type_special_day_periods == ["vacation", "businessTrip"]


async def test_unit_calendar_settings_parses_contract(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/calendars/unitCalendarSettings/11", body=_UNIT_CALENDAR)
    async with CalendarsClient(config=token_config) as ips:
        cal = await ips.unit_calendar_settings(11)

    assert cal.calendar_id == 9
    assert cal.owner == "organizationUnit"
    assert cal.unit_id == 11
    assert cal.standard_week == {"weekDays": []}
    # standardWorkPeriods / specialCalendarDays пришли null -> пустые списки
    assert cal.standard_work_periods == []
    assert cal.special_calendar_days == []
