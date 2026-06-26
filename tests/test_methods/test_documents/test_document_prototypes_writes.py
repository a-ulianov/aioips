"""Тесты мутаций прототипов документов: create / update (раздел documents)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.client import IPSClient

_Client = IPSClient


async def test_update_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.update_document_prototypes(1742)
    assert fake_ips.requests == []


async def test_update_confirm_true_posts_empty_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/api/documents/prototypes/1742", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.update_document_prototypes(1742, confirm=True)
    assert result is None
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/api/documents/prototypes/1742"
    assert req.body == {}


async def test_create_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.create_document_prototypes(1116)
    assert fake_ips.requests == []


async def test_create_confirm_true_returns_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/api/documents/1116/prototypes/create",
        body={"id": 55, "name": "Шаблон"},
    )
    async with _Client(config=token_config) as ips:
        result = await ips.create_document_prototypes(1116, confirm=True)
    assert result == {"id": 55, "name": "Шаблон"}
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/api/documents/1116/prototypes/create"
    assert req.body == {}


async def test_create_null_body_to_empty_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/api/documents/1116/prototypes/create", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.create_document_prototypes(1116, confirm=True)
    assert result == {}
