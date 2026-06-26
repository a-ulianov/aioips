"""Тесты метода ``edit_search_scheme`` (правка поисковой схемы, мутация)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.client import IPSClient

_Client = IPSClient

_SCHEME = {"searchSchemaName": "По деталям", "searchedObjectTypes": [5], "columns": []}


async def test_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.edit_search_scheme(102550, _SCHEME)
    assert fake_ips.requests == []


async def test_confirm_true_returns_true(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/searchSchemes/102550/edit", body=True)
    async with _Client(config=token_config) as ips:
        result = await ips.edit_search_scheme(102550, _SCHEME, confirm=True)
    assert result is True
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/core/api/searchSchemes/102550/edit"
    assert req.body == _SCHEME


async def test_confirm_true_returns_false(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/searchSchemes/102550/edit", body=False)
    async with _Client(config=token_config) as ips:
        result = await ips.edit_search_scheme(102550, _SCHEME, confirm=True)
    assert result is False
