"""Тесты метода ``object_set_modify_content_date`` (мутация даты модификации контента)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.client import IPSClient

_Client = IPSClient


async def test_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.object_set_modify_content_date(102550)
    # Без confirm запрос не должен уйти на сервер.
    assert fake_ips.requests == []


async def test_confirm_true_posts_empty_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/objects/102550/setModifyContentDate", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.object_set_modify_content_date(102550, confirm=True)
    assert result is None
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/core/api/objects/102550/setModifyContentDate"
    assert req.body == {}
