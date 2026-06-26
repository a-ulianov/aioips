"""Тесты методов раздела Портфеля (briefcase): статус и отмена."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig


async def test_briefcase_status_parses(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {"percent": 42, "status": "Экспорт объектов", "isCompleted": False}
    fake_ips.add("post", "/core/api/briefcase/GetStatus", body=body)
    async with IPSClient(config=token_config) as ips:
        state = await ips.briefcase_status()

    assert state.percent == 42
    assert state.status == "Экспорт объектов"
    assert state.is_completed is False
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/briefcase/GetStatus"
    assert req.body == {}


async def test_briefcase_status_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/briefcase/GetStatus",
        body={"percent": 0, "status": None, "isCompleted": False},
    )
    async with IPSClient(config=token_config) as ips:
        state = await ips.briefcase_status()

    assert state.percent == 0
    assert state.status is None
    assert state.is_completed is False


async def test_briefcase_export_progress_parses(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {"percent": 100, "status": "Готово", "isCompleted": True}
    fake_ips.add("post", "/core/api/briefcase/GetExportProgress", body=body)
    async with IPSClient(config=token_config) as ips:
        progress = await ips.briefcase_export_progress()

    assert progress.percent == 100
    assert progress.is_completed is True
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/briefcase/GetExportProgress"
    assert req.body == {}


async def test_briefcase_check_metadata_result_parses(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {
        "errorMessage": "Расхождение метаданных",
        "checkMetadataErrors": [
            {"type": "error", "category": 1, "itemTextCategory": "Тип объекта"},
        ],
    }
    fake_ips.add("post", "/core/api/briefcase/CheckMetadataResult", body=body)
    async with IPSClient(config=token_config) as ips:
        result = await ips.briefcase_check_metadata_result()

    assert result.error_message == "Расхождение метаданных"
    assert len(result.check_metadata_errors) == 1
    assert result.check_metadata_errors[0]["type"] == "error"
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/briefcase/CheckMetadataResult"
    assert req.body == {}


async def test_briefcase_check_metadata_result_null_errors(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    body = {"errorMessage": None, "checkMetadataErrors": None}
    fake_ips.add("post", "/core/api/briefcase/CheckMetadataResult", body=body)
    async with IPSClient(config=token_config) as ips:
        result = await ips.briefcase_check_metadata_result()

    assert result.error_message is None
    assert result.check_metadata_errors == []


async def test_briefcase_cancel_export_void(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/briefcase/CancelExport", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.briefcase_cancel_export()

    assert result is None
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/briefcase/CancelExport"
    assert req.body == {}


async def test_briefcase_cancel_import_void(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/briefcase/CancelImport", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.briefcase_cancel_import()

    assert result is None
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/briefcase/CancelImport"
    assert req.body == {}


async def test_briefcase_check_metadata_cancel_void(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/briefcase/CheckMetadataCancel", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.briefcase_check_metadata_cancel()

    assert result is None
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/briefcase/CheckMetadataCancel"
    assert req.body == {}
