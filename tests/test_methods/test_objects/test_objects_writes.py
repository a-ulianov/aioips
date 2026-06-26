"""Тесты мутирующих write-методов раздела объектов IPS Web API."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig


async def test_create_object_version_unwraps_object_dto(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/CreateObjectVersion/102550",
        body={
            "result": {"objectID": 102550, "id": -9, "isCreationMode": False},
            "modificationsHistory": [],
        },
    )
    async with IPSClient(config=token_config) as ips:
        draft = await ips.object_create_object_version(102550, log_history=False)
    assert draft.object_id == 102550
    req = next(r for r in fake_ips.requests if "CreateObjectVersion" in r.path)
    assert req.body == {}
    assert req.query["isNeedToLogModificationHistory"] == "false"


async def test_edit_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/102550/edit",
        body={"result": None, "modificationsHistory": []},
    )
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_edit(102550) is None
    req = next(r for r in fake_ips.requests if r.path.endswith("/edit"))
    assert req.body == {}
    assert req.query["isNeedToLogModificationHistory"] == "true"


async def test_cancel_changes_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm"):
            await ips.object_cancel_changes([102550])
    # без confirm запрос НЕ должен уходить
    assert all("cancelChanges" not in r.path for r in fake_ips.requests)


async def test_cancel_changes_with_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/cancelChanges",
        body={"result": [102550, 102551], "modificationsHistory": []},
    )
    async with IPSClient(config=token_config) as ips:
        done = await ips.object_cancel_changes(
            [102550, 102551], confirm=True, admin_mode=True, ignore_exceptions=False
        )
    assert done == [102550, 102551]
    req = next(r for r in fake_ips.requests if "cancelChanges" in r.path)
    assert req.body == [102550, 102551]
    assert req.query["isAdminMode"] == "true"
    assert req.query["isNeedToIgnoreExceptions"] == "false"


async def test_include_in_composition_returns_relations(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/102551/includeInComposition",
        body={
            "result": [
                {"relationID": 1, "projID": 102551, "partID": 33001, "relationType": 1},
                {"relationID": 2, "projID": 102551, "partID": 33002, "relationType": 1},
            ],
            "modificationsHistory": [],
        },
    )
    async with IPSClient(config=token_config) as ips:
        relations = await ips.object_include_in_composition(102551, [33001, 33002])
    assert [r.part_id for r in relations] == [33001, 33002]
    req = next(r for r in fake_ips.requests if "includeInComposition" in r.path)
    assert req.body == [33001, 33002]


async def test_make_base_versions_returns_int_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/makeBaseVersion",
        body={"result": [33001, 33002], "modificationsHistory": []},
    )
    async with IPSClient(config=token_config) as ips:
        done = await ips.object_make_base_versions([33001, 33002], ignore_exceptions=True)
    assert done == [33001, 33002]
    req = next(r for r in fake_ips.requests if r.path == "/core/api/objects/makeBaseVersion")
    assert req.body == [33001, 33002]
    assert req.query["isNeedToIgnoreExceptions"] == "true"


async def test_make_base_version_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/33001/makeBaseVersion",
        body={"result": None, "modificationsHistory": []},
    )
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_make_base_version(33001) is None
    req = next(r for r in fake_ips.requests if r.path == "/core/api/objects/33001/makeBaseVersion")
    assert req.body == {}


async def test_connect_to_object_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/102550/connectToObject",
        body={"result": 7, "modificationsHistory": []},
    )
    async with IPSClient(config=token_config) as ips:
        code = await ips.object_connect_to_object(102550, to_object_id=102560)
    assert code == 7
    req = next(r for r in fake_ips.requests if "connectToObject" in r.path)
    assert req.body == {}
    assert req.query["toObjectId"] == "102560"


async def test_check_in_command_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/-777/checkInCommand",
        body={"result": 778, "modificationsHistory": []},
    )
    async with IPSClient(config=token_config) as ips:
        new_version = await ips.object_check_in_command(-777, preserve_working_copies=True)
    assert new_version == 778
    req = next(r for r in fake_ips.requests if "checkInCommand" in r.path)
    assert req.body == {}
    assert req.query["preserveWorkingCopies"] == "true"


async def test_validate_set_next_lc_step_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/102550/validateSetNextLCStep",
        body={"result": None, "modificationsHistory": []},
    )
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_validate_set_next_lc_step(102550, next_step_id=42) is None
    req = next(r for r in fake_ips.requests if "validateSetNextLCStep" in r.path)
    assert req.body == {}
    assert req.query["nextStepId"] == "42"
