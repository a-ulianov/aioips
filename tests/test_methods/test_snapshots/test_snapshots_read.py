"""Тесты методов чтения раздела снимков состава (snapshots).

Раздел ``snapshots`` не подключён к публичному ``IPSClient``, поэтому тесты
работают с агрегатором :class:`SnapshotsAPI` напрямую (он наследует ядро
``APIManager`` и является асинхронным контекстным менеджером).
"""

from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.methods.snapshots import SnapshotsAPI


async def test_snapshot_composition_returns_version_ids(token_config: IPSConfig, fake_ips: FakeIPS):
    body = [1001, 1002, 1003]
    fake_ips.add("get", "/core/api/snapshots/45012/composition", body=body)
    async with SnapshotsAPI(config=token_config) as ips:
        composition = await ips.snapshot_composition(45012)

    assert composition == [1001, 1002, 1003]
    assert all(isinstance(item, int) for item in composition)


async def test_snapshot_composition_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/snapshots/7/composition", body=[])
    async with SnapshotsAPI(config=token_config) as ips:
        composition = await ips.snapshot_composition(7)

    assert composition == []
