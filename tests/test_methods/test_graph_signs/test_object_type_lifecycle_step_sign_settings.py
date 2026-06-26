"""Тесты чтения настроек подписей шага ЖЦ для типа объекта."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient


async def test_returns_groups(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/api/objectTypes/1742/lifecycleSteps/5/signs"
    fake_ips.add("get", path, body=[{"name": "Группа 1", "graphs": [{"id": 7}]}])
    async with _Client(config=token_config) as ips:
        groups = await ips.object_type_lifecycle_step_sign_settings(1742, 5)
    assert len(groups) == 1
    assert groups[0].name == "Группа 1"
    req = fake_ips.requests[-1]
    assert req.path == path
    assert req.method == "GET"


async def test_empty_response(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/api/objectTypes/1/lifecycleSteps/2/signs", body=None)
    async with _Client(config=token_config) as ips:
        groups = await ips.object_type_lifecycle_step_sign_settings(1, 2)
    assert groups == []
