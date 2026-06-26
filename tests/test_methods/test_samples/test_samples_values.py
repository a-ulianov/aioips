"""Тесты бинарных/числовых чтений значений (samples/values).

Бинарные методы проверяют возврат ``bytes``; числовой — путь и распаковку
``int`` против поддельного сервера :class:`FakeIPS`.
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient


async def test_sample_value_as_file_returns_bytes(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/samples/values/demo.bin/asFile"
    fake_ips.add("get", path, body=b"\x01\x02\x03FILE\xff")
    async with _Client(config=token_config) as ips:
        data = await ips.sample_value_as_file("demo.bin")

    assert data == b"\x01\x02\x03FILE\xff"
    assert fake_ips.requests[-1].path == path


async def test_sample_value_as_content_returns_bytes(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/samples/values/demo.bin/asContent"
    fake_ips.add("get", path, body=b"CONTENT\x00")
    async with _Client(config=token_config) as ips:
        data = await ips.sample_value_as_content("demo.bin")

    assert data == b"CONTENT\x00"
    assert fake_ips.requests[-1].path == path


async def test_sample_value_as_long_roundtrip(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/samples/values/42/asLong"
    fake_ips.add("get", path, body=42)
    async with _Client(config=token_config) as ips:
        n = await ips.sample_value_as_long(42)

    assert n == 42
    assert isinstance(n, int)
    assert fake_ips.requests[-1].path == path
