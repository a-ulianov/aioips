"""Тесты мутирующих методов календарей (confirm-гейты + сериализация тела)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient


async def test_update_calendar_settings_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError):
            await ips.update_calendar_settings({"calendarId": 1})
    assert fake_ips.requests == []


async def test_update_calendar_settings_posts_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/calendars/calendarSettings", body=None)
    body = {"calendarId": 1, "caption": "Раб"}
    async with _Client(config=token_config) as ips:
        result = await ips.update_calendar_settings(body, confirm=True)
    assert result is None
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/calendars/calendarSettings"
    assert req.body == body


async def test_update_user_calendar_settings_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError):
            await ips.update_user_calendar_settings({"calendarId": 2})
    assert fake_ips.requests == []


async def test_update_user_calendar_settings_posts_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/calendars/userCalendarSettings", body=None)
    async with _Client(config=token_config) as ips:
        await ips.update_user_calendar_settings({"calendarId": 2}, confirm=True)
    assert fake_ips.requests[-1].path == "/core/api/calendars/userCalendarSettings"


async def test_set_base_calendar_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError):
            await ips.set_base_calendar(102550, 1)
    assert fake_ips.requests == []


async def test_set_base_calendar_path_and_empty_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/calendars/setBaseCalendar/102550/1", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.set_base_calendar(102550, 1, confirm=True)
    assert result is None
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/calendars/setBaseCalendar/102550/1"
    assert req.body == {}
