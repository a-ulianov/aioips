"""Тесты метода раздела уведомлений."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.notify import NotificationMessage, WayOfNotification

_Client = IPSClient


async def test_send_notification_sends_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/notify/SendNotification", body=None)
    notification = NotificationMessage(
        user_id=42,
        title="Готово",
        message="Документ согласован.",
        way_of_notification=WayOfNotification.INTERNAL_MAIL,
    )
    async with _Client(config=token_config) as ips:
        result = await ips.send_notification(notification)

    assert result is None
    sent = fake_ips.requests[-1]
    assert sent.method == "POST"
    assert sent.path == "/core/api/notify/SendNotification"
    assert sent.body == {
        "userId": 42,
        "title": "Готово",
        "message": "Документ согласован.",
        "wayOfNotification": "internalMail",
    }


async def test_send_notification_defaults_way_and_omits_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/notify/SendNotification", body=None)
    notification = NotificationMessage(user_id=7)
    async with _Client(config=token_config) as ips:
        await ips.send_notification(notification)

    sent = fake_ips.requests[-1]
    assert sent.body == {
        "userId": 7,
        "wayOfNotification": "internalAndExternalMail",
    }
