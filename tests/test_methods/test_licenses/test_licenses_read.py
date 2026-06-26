"""Тесты методов чтения раздела лицензий."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig


async def test_generate_client_id_returns_string(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/licenses/generateClientId", body="CLIENT-ABC-123")
    async with IPSClient(config=token_config) as ips:
        client_id = await ips.generate_client_id()

    assert client_id == "CLIENT-ABC-123"


async def test_generate_client_id_none_to_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/licenses/generateClientId", body=None)
    async with IPSClient(config=token_config) as ips:
        client_id = await ips.generate_client_id()

    assert client_id == ""
