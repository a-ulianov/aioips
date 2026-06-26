"""Тесты записи настроек документов типа (confirm-гейт + сериализация тела)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient


async def test_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError):
            await ips.save_document_settings(1742, {"objectTypeId": 1742})
    assert fake_ips.requests == []


async def test_posts_body_with_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/api/documents/1742/settings"
    fake_ips.add("post", path, body=None)
    body = {"objectTypeId": 1742, "useDocuments": True}
    async with _Client(config=token_config) as ips:
        result = await ips.save_document_settings(1742, body, confirm=True)
    assert result is None
    req = fake_ips.requests[-1]
    assert req.path == path
    assert req.body == body
