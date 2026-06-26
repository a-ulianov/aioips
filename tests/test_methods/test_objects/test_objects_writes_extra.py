"""Тесты дополнительных write-методов раздела объектов IPS Web API (сложные тела)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.objects import (
    AddObjectsByTemplateBody,
    AttributeValues,
    CreateObjectByPrototype,
    SetAttributeValuesExBody,
)


async def test_create_by_prototype_unwraps_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/CreateByPrototype",
        body={
            "result": {
                "objectDto": {"objectID": -9, "id": -9, "isCreationMode": True},
                "relatedObjectIds": [33001, 33002],
            },
            "modificationsHistory": [],
        },
    )
    async with IPSClient(config=token_config) as ips:
        created = await ips.object_create_by_prototype(
            CreateObjectByPrototype(prototype_id=102550, is_article=True),
            log_history=False,
        )
    assert created["relatedObjectIds"] == [33001, 33002]
    req = next(r for r in fake_ips.requests if "CreateByPrototype" in r.path)
    # тело: алиасы camelCase, exclude_none — contextRule/currentProjectDto не передаются
    assert req.body == {"prototypeId": 102550, "isArticle": True}
    assert req.query["isNeedToLogModificationHistory"] == "false"


async def test_exclude_from_composition_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm"):
            await ips.object_exclude_from_composition([55001])
    assert all("excludeFromComposition" not in r.path for r in fake_ips.requests)


async def test_exclude_from_composition_with_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/excludeFromComposition",
        body={"result": [55001, 55002], "modificationsHistory": []},
    )
    async with IPSClient(config=token_config) as ips:
        removed = await ips.object_exclude_from_composition(
            [55001, 55002], confirm=True, delete_relation_mode=1, ignore_exceptions=True
        )
    assert removed == [55001, 55002]
    req = next(r for r in fake_ips.requests if "excludeFromComposition" in r.path)
    assert req.body == {"relationIds": [55001, 55002], "deleteRelationMode": 1}
    assert req.query["isNeedToIgnoreExceptions"] == "true"


async def test_set_attribute_values_ex_unwraps_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/102550/attributeValuesEx",
        body={"result": {"12": {"message": "ok"}}, "modificationsHistory": []},
    )
    async with IPSClient(config=token_config) as ips:
        errors = await ips.object_set_attribute_values_ex(
            102550,
            SetAttributeValuesExBody(
                attribute_values=[AttributeValues(attribute_id=12, values=["550.07.305"])],
                return_delta=True,
            ),
        )
    assert errors == {"12": {"message": "ok"}}
    req = next(r for r in fake_ips.requests if "attributeValuesEx" in r.path)
    assert req.body["returnDelta"] is True
    assert req.body["attributeValues"][0]["attributeId"] == 12
    assert req.query["isNeedToLogModificationHistory"] == "true"


async def test_add_objects_by_template_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/102551/addObjectsByTemplate",
        body={"result": None, "modificationsHistory": []},
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_add_objects_by_template(
            102551,
            AddObjectsByTemplateBody(template_id=701, object_ids=[[33001], [33002]]),
        )
    assert result is None
    req = next(r for r in fake_ips.requests if "addObjectsByTemplate" in r.path)
    assert req.body == {"templateId": 701, "objectIds": [[33001], [33002]]}


async def test_check_out_with_check_modify_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/102550/checkOutWithCheckModify",
        body={"result": -777, "modificationsHistory": []},
    )
    async with IPSClient(config=token_config) as ips:
        working_id = await ips.object_check_out_with_check_modify(102550)
    assert working_id == -777
    req = next(r for r in fake_ips.requests if "checkOutWithCheckModify" in r.path)
    assert req.body == {}
    assert req.query["isNeedToLogModificationHistory"] == "true"


async def test_can_set_next_lc_step_returns_tuple(token_config: IPSConfig, fake_ips: FakeIPS):
    # КИРИЛЛИЧЕСКАЯ с (U+0441) в пути — баг IPS API; путь регистрируется ровно так же.
    fake_ips.add(
        "post",
        "/core/api/objects/102550/сanSetNextLCStep",
        body={
            "result": {"item1": False, "item2": "не пройдены условия"},
            "modificationsHistory": [],
        },
    )
    async with IPSClient(config=token_config) as ips:
        check = await ips.object_can_set_next_lc_step(102550, next_step_id=42)
    assert check["item1"] is False
    assert check["item2"] == "не пройдены условия"
    req = next(r for r in fake_ips.requests if "anSetNextLCStep" in r.path)
    # путь, дошедший до сервера, содержит кириллическую с (U+0441)
    assert "сanSetNextLCStep" in req.path
    assert req.body == {}
    assert req.query["nextStepId"] == "42"
