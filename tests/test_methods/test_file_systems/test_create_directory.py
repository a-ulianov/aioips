"""Тесты метода ``create_directory`` (создание каталога на ФС сервера, мутация)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.client import IPSClient

_Client = IPSClient


async def test_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.create_directory("D:\\export\\batch")
    assert fake_ips.requests == []


async def test_confirm_true_posts_path_query(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/fileSystems/createDirectory", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.create_directory("D:\\export\\batch", confirm=True)
    assert result is None
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/core/api/fileSystems/createDirectory"
    assert req.query["path"] == "D:\\export\\batch"
