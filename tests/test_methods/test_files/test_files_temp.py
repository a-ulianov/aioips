"""Тесты загрузки и удаления временных файлов (multipart)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig


async def test_upload_temp_file_returns_name(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/files/temp", body="temp_ab12.pdf")
    async with IPSClient(config=token_config) as ips:
        name = await ips.upload_temp_file(b"%PDF-1.4 data", "schema.pdf")

    assert name == "temp_ab12.pdf"
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/files/temp"
    assert request.method == "POST"


async def test_upload_temp_file_with_packed_flag(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/files/temp", body="t.bin")
    async with IPSClient(config=token_config) as ips:
        name = await ips.upload_temp_file(b"bytes", "t.bin", is_already_packed=True)

    assert name == "t.bin"


async def test_upload_temp_file_none_to_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/files/temp", body=None)
    async with IPSClient(config=token_config) as ips:
        name = await ips.upload_temp_file(b"x", "x")

    assert name == ""


async def test_delete_temp_file_uses_encoded_path(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("delete", "/core/api/files/temp/temp ab.pdf", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.delete_temp_file("temp ab.pdf")

    assert result is None
    assert fake_ips.requests[-1].method == "DELETE"
