"""Тесты методов записи атрибутов объекта (set/delete/cleanup/temp)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.objects import Attribute, AttributeValues

OBJ = 102550
SET_VALUES_URL = f"/core/api/objects/{OBJ}/attributeValues"
SET_ATTRS_URL = f"/core/api/objects/{OBJ}/attributes"
DELETE_URL = f"/core/api/objects/{OBJ}/attributes/12"
CLEANUP_URL = f"/core/api/objects/{OBJ}/attributes/12/cleanup"
TEMP_URL = f"/core/api/objects/{OBJ}/attributes/tempAttribute"


async def test_set_attribute_values_builds_body_and_unwraps(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "post",
        SET_VALUES_URL,
        body={
            "result": [{"attributeId": 12, "attributeType": "ftString", "values": ["550.07.305"]}],
            "modificationsHistory": [{"actionID": "edit", "categoryID": OBJ}],
        },
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_set_attribute_values(
            OBJ,
            [AttributeValues(attribute_id=12, values=["550.07.305"])],
            delete_not_existing=True,
            return_delta=True,
        )

    # Результат разворачивается из поля result.
    assert len(result) == 1
    assert result[0].attribute_id == 12
    assert result[0].values == ["550.07.305"]

    request = next(r for r in fake_ips.requests if r.path == SET_VALUES_URL)
    body = request.body
    assert body["deleteNotExistingAttribute"] is True
    assert body["dontDeleteBlobs"] is False
    assert body["returnDelta"] is True
    av = body["attributeValues"][0]
    assert av["attributeId"] == 12  # lowercase camelCase для AttributeValues
    assert av["values"] == ["550.07.305"]


async def test_set_attribute_values_empty_result(token_config: IPSConfig, fake_ips: FakeIPS):
    # result==null (ничего не изменилось) должно дать пустой список, а не падение.
    fake_ips.add("post", SET_VALUES_URL, body={"result": None, "modificationsHistory": None})
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_set_attribute_values(OBJ, [], log_history=False)

    assert result == []
    request = next(r for r in fake_ips.requests if r.path == SET_VALUES_URL)
    assert request.body["attributeValues"] == []


async def test_set_attributes_builds_array_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        SET_ATTRS_URL,
        body={
            "result": [{"attributeID": 12, "values": ["550.07.305"]}],
            "modificationsHistory": None,
        },
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_set_attributes(
            OBJ, [Attribute(attribute_id=12, values=["550.07.305"])]
        )

    assert len(result) == 1
    assert result[0].attribute_id == 12

    request = next(r for r in fake_ips.requests if r.path == SET_ATTRS_URL)
    body = request.body
    assert isinstance(body, list)  # тело — голый массив
    assert body[0]["attributeID"] == 12  # uppercase alias для Attribute
    assert body[0]["values"] == ["550.07.305"]


async def test_delete_attribute_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.object_delete_attribute(OBJ, 12)

    # Без confirm HTTP-запрос не должен выполняться.
    assert not any(r.path == DELETE_URL for r in fake_ips.requests)


async def test_delete_attribute_with_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("delete", DELETE_URL, body={"result": {}, "modificationsHistory": None})
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_delete_attribute(OBJ, 12, confirm=True)

    assert result is None
    assert any(r.path == DELETE_URL and r.method == "DELETE" for r in fake_ips.requests)


async def test_cleanup_attribute_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.object_cleanup_attribute(OBJ, 12)

    assert not any(r.path == CLEANUP_URL for r in fake_ips.requests)


async def test_cleanup_attribute_with_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("delete", CLEANUP_URL, body={"result": {}, "modificationsHistory": None})
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_cleanup_attribute(OBJ, 12, confirm=True)

    assert result is None
    assert any(r.path == CLEANUP_URL and r.method == "DELETE" for r in fake_ips.requests)


async def test_add_temporary_attribute_builds_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        TEMP_URL,
        body={"attributeID": 12, "dataType": "ftString", "values": ["tmp"]},
    )
    async with IPSClient(config=token_config) as ips:
        attr = await ips.object_add_temporary_attribute(
            OBJ, 12, fail_if_exists=True, values=["tmp"]
        )

    # Ответ — голый AttributeDto (без обёртки result).
    assert attr.attribute_id == 12
    assert attr.values == ["tmp"]

    request = next(r for r in fake_ips.requests if r.path == TEMP_URL)
    body = request.body
    assert body["attributeId"] == 12
    assert body["failIfExists"] is True
    assert body["values"] == ["tmp"]


async def test_add_temporary_attribute_defaults_values_empty(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", TEMP_URL, body={"attributeID": 12, "values": None})
    async with IPSClient(config=token_config) as ips:
        await ips.object_add_temporary_attribute(OBJ, 12)

    request = next(r for r in fake_ips.requests if r.path == TEMP_URL)
    assert request.body["values"] == []
    assert request.body["failIfExists"] is False
