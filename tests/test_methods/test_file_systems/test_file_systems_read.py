"""Тесты методов чтения раздела файловых систем."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig


async def test_local_drives_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    drives = ["C:\\", "D:\\", "X:\\"]
    fake_ips.add("get", "/core/api/fileSystems/localDrives", body=drives)
    async with IPSClient(config=token_config) as ips:
        result = await ips.local_drives()

    assert result == drives


async def test_local_drives_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/fileSystems/localDrives", body=[])
    async with IPSClient(config=token_config) as ips:
        result = await ips.local_drives()

    assert result == []
