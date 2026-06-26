"""Тесты мутирующих write-методов раздела снимков состава (snapshots)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.snapshots import CreateSnapshot, UpdateSnapshot


async def test_create_snapshot_sends_body_and_returns_int(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    # Ответ — «голое» целое (id снимка), не обёрнутое в {"result": ...}.
    fake_ips.add("post", "/core/api/snapshots", body=9001)
    async with IPSClient(config=token_config) as ips:
        snapshot_id = await ips.create_snapshot(
            CreateSnapshot(
                snapshot_name="Релиз 1.0",
                composition_object_version_ids=[45012, 45013],
            )
        )
    assert snapshot_id == 9001
    req = next(r for r in fake_ips.requests if r.path == "/core/api/snapshots")
    assert req.method == "POST"
    assert req.body == {
        "snapshotName": "Релиз 1.0",
        "compositionObjectVersionIds": [45012, 45013],
    }


async def test_create_snapshot_none_response_returns_zero(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    # Пустое тело ответа → возврат 0.
    fake_ips.add("post", "/core/api/snapshots", body=None)
    async with IPSClient(config=token_config) as ips:
        snapshot_id = await ips.create_snapshot(CreateSnapshot(snapshot_name="X"))
    assert snapshot_id == 0


async def test_update_snapshot_puts_to_path_and_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("put", "/core/api/snapshots/9001", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.update_snapshot(
            9001,
            UpdateSnapshot(
                snapshot_name="Релиз 1.1",
                composition_object_version_ids=[45012, 45013, 45014],
            ),
        )
    assert result is None
    req = next(r for r in fake_ips.requests if r.path == "/core/api/snapshots/9001")
    assert req.method == "PUT"
    assert req.body == {
        "snapshotName": "Релиз 1.1",
        "compositionObjectVersionIds": [45012, 45013, 45014],
    }


async def test_delete_snapshot_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm"):
            await ips.delete_snapshot(9001)
    # без confirm запрос НЕ должен уходить
    assert all("/core/api/snapshots/9001" not in r.path for r in fake_ips.requests)


async def test_delete_snapshot_with_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("delete", "/core/api/snapshots/9001", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.delete_snapshot(9001, confirm=True)
    assert result is None
    req = next(r for r in fake_ips.requests if r.path == "/core/api/snapshots/9001")
    assert req.method == "DELETE"
    assert req.body == {}
