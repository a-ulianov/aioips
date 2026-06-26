"""Тесты доп. методов раздела объектов: checkout-сервис, видимость, print/save."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.visibilities import VisibilitySettings


async def test_load_descriptions_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/ObjectsCheckOutServerService/LoadDescriptions",
        body=[
            {"caption": "Деталь", "objectTypeID": 5, "objectID": 9001, "id": 102550, "mode": 0},
        ],
    )
    async with IPSClient(config=token_config) as ips:
        descrs = await ips.object_load_descriptions([102550, 102551])
    assert descrs[0]["caption"] == "Деталь"
    req = next(r for r in fake_ips.requests if "LoadDescriptions" in r.path)
    # Тело — голый массив id версий.
    assert req.body == [102550, 102551]
    assert req.query["throwException"] == "false"


async def test_check_out_versions_returns_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/ObjectsCheckOutServerService/CheckOut",
        body={"objects": [{"id": 102550}], "pairVersionSources": None, "pairVersionTargets": None},
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_check_out_versions([102550], throw_exception=True)
    assert result["objects"][0]["id"] == 102550
    req = next(r for r in fake_ips.requests if r.path.endswith("/CheckOut"))
    assert req.body == [102550]
    assert req.query["throwException"] == "true"


async def test_rollback_check_out_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/objects/ObjectsCheckOutServerService/Rollback", body=None)
    payload = {"objects": [{"id": 102550}]}
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_rollback_check_out(payload)
    assert result is None
    req = next(r for r in fake_ips.requests if r.path.endswith("/Rollback"))
    # Тело — словарь результата CheckOut, передан как есть.
    assert req.body == payload


async def test_check_access_rights_for_visibility_returns_str(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/objects/visibilities/checkAccessRights", body="editorMode")
    async with IPSClient(config=token_config) as ips:
        mode = await ips.object_check_access_rights_for_visibility([102550])
    assert mode == "editorMode"
    req = next(r for r in fake_ips.requests if "checkAccessRights" in r.path)
    assert req.body == [102550]


async def test_update_visibility_settings_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/objects/102550/visibilities", body=None)
    settings = [VisibilitySettings(objectType=5, objectName="Узел", objectId=9001, isHidden=True)]
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_update_visibility_settings(102550, settings)
    assert result is None
    req = next(r for r in fake_ips.requests if r.path == "/core/api/objects/102550/visibilities")
    assert req.method == "POST"
    # Тело — голый массив VisibilitySettingsDto.
    assert isinstance(req.body, list)
    assert req.body[0]["objectName"] == "Узел"
    assert req.body[0]["isHidden"] is True


async def test_print_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/objects/102550/print", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_print(102550)
    assert result is None
    req = next(r for r in fake_ips.requests if r.path.endswith("/print"))
    assert req.body == {}


async def test_save_to_disk_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/objects/102550/saveToDisk", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_save_to_disk(102550)
    assert result is None
    req = next(r for r in fake_ips.requests if r.path.endswith("/saveToDisk"))
    assert req.body == {}


async def test_save_to_arc_copy_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/102550/saveToArcCopy",
        body={"result": None, "modificationsHistory": []},
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_save_to_arc_copy(102550, log_history=False)
    assert result is None
    req = next(r for r in fake_ips.requests if r.path.endswith("/saveToArcCopy"))
    assert req.body == {}
    assert req.query["isNeedToLogModificationHistory"] == "false"
