"""Тесты методов чтения раздела почтового агента."""

from datetime import datetime

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig


async def test_mail_agent_settings_returns_settings(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {"unreadMail": {"checkInterval": 10}}
    fake_ips.add("get", "/core/api/MailAgent/settings", body=body)
    async with IPSClient(config=token_config) as ips:
        settings = await ips.mail_agent_settings()

    assert settings.unread_mail.check_interval == 10


async def test_mail_agent_settings_default_interval(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/MailAgent/settings", body={"unreadMail": {}})
    async with IPSClient(config=token_config) as ips:
        settings = await ips.mail_agent_settings()

    assert settings.unread_mail.check_interval == 5


async def test_unread_mail_returns_counts(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {
        "highCount": 2,
        "normalCount": 7,
        "lowCount": 1,
        "lastCheckTime": "2026-06-24T08:30:00Z",
    }
    fake_ips.add("get", "/core/api/MailAgent/mailbox/unreadMail", body=body)
    async with IPSClient(config=token_config) as ips:
        mail = await ips.unread_mail()

    assert mail.high_count == 2
    assert mail.normal_count == 7
    assert mail.low_count == 1
    assert mail.last_check_time == datetime.fromisoformat("2026-06-24T08:30:00+00:00")
