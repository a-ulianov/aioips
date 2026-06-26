"""Тесты записи настроек просмотра/печати типа объекта (confirm-гейт + тело)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient


async def test_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError):
            await ips.set_view_print_settings(1742, {"injectSigns": True})
    assert fake_ips.requests == []


async def test_posts_body_with_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/settings/view/1742/setSettings"
    fake_ips.add("post", path, body=None)
    body = {"injectSigns": True, "injectFileChecksum": False}
    async with _Client(config=token_config) as ips:
        result = await ips.set_view_print_settings(1742, body, confirm=True)
    assert result is None
    req = fake_ips.requests[-1]
    assert req.path == path
    assert req.body == body
