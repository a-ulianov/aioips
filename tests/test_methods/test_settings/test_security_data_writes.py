"""Тесты мутаций данных безопасности: addOrUpdate / remove (раздел settings)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.client import IPSClient

_Client = IPSClient

_RECORD = {"userId": 4210, "securityGroup": {"id": 3, "name": "Operators"}}


async def test_add_or_update_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.add_or_update_security_data(_RECORD)
    assert fake_ips.requests == []


async def test_add_or_update_confirm_true_posts_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/settings/addOrUpdateSecurityData", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.add_or_update_security_data(_RECORD, confirm=True)
    assert result is None
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/core/api/settings/addOrUpdateSecurityData"
    assert req.body == _RECORD


async def test_remove_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.remove_security_data(user_id=4210)
    assert fake_ips.requests == []


async def test_remove_confirm_true_posts_query_empty_body(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/settings/removeSecurityData", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.remove_security_data(user_id=4210, confirm=True)
    assert result is None
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/core/api/settings/removeSecurityData"
    assert req.body == {}
    assert req.query["userId"] == "4210"


async def test_remove_user_id_omitted_when_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/settings/removeSecurityData", body=None)
    async with _Client(config=token_config) as ips:
        await ips.remove_security_data(confirm=True)
    req = fake_ips.requests[-1]
    assert "userId" not in req.query
