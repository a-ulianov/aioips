"""Тесты мутирующих методов раздела Портфеля (запуск проверок/экспорта/импорта)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient


async def test_check_metadata_only_start_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.briefcase_check_metadata_only_start(briefcase_path="X:/p.brief")

    assert fake_ips.requests == []


async def test_check_metadata_only_start_sends_query(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/briefcase/CheckMetadataOnlyStart", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.briefcase_check_metadata_only_start(
            briefcase_path="X:/p.brief", system_only=True, confirm=True
        )

    assert result is None
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/briefcase/CheckMetadataOnlyStart"
    assert request.query["briefcasePath"] == "X:/p.brief"
    assert request.query["systemOnly"] == "true"
    assert "briefcaseId" not in request.query


async def test_check_metadata_start_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.briefcase_check_metadata_start({"path": "X:/p.brief"})

    assert fake_ips.requests == []


async def test_check_metadata_start_sends_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/briefcase/CheckMetadataStart", body=None)
    async with _Client(config=token_config) as ips:
        await ips.briefcase_check_metadata_start({"path": "X:/p.brief"}, confirm=True)

    request = fake_ips.requests[-1]
    assert request.path == "/core/api/briefcase/CheckMetadataStart"
    assert request.body == {"path": "X:/p.brief"}


async def test_start_export_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.briefcase_start_export({"path": "X:/p.brief"})

    assert fake_ips.requests == []


async def test_start_export_sends_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/briefcase/StartExport", body=None)
    async with _Client(config=token_config) as ips:
        await ips.briefcase_start_export({"path": "X:/p.brief", "comment": "c"}, confirm=True)

    request = fake_ips.requests[-1]
    assert request.path == "/core/api/briefcase/StartExport"
    assert request.body == {"path": "X:/p.brief", "comment": "c"}


async def test_start_import_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.briefcase_start_import({"path": "X:/p.brief"})

    assert fake_ips.requests == []


async def test_start_import_sends_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/briefcase/StartImport", body=None)
    async with _Client(config=token_config) as ips:
        await ips.briefcase_start_import({"path": "X:/p.brief", "createOnly": True}, confirm=True)

    request = fake_ips.requests[-1]
    assert request.path == "/core/api/briefcase/StartImport"
    assert request.body == {"path": "X:/p.brief", "createOnly": True}
