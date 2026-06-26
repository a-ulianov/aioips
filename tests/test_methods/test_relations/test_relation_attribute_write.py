"""Тесты write-методов атрибутов связи (set/setValues/tempAttribute)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.objects import Attribute, AttributeValues

SET_ATTRS_URL = "/core/api/relations/700123/attributes"
SET_VALUES_URL = "/core/api/relations/700123/attributeValues"
TEMP_ATTR_URL = "/core/api/relations/700123/attributes/tempAttribute"


async def test_relation_set_attributes_builds_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        SET_ATTRS_URL,
        body={"result": [{"attributeID": 205, "values": ["A1"]}], "modificationsHistory": None},
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.relation_set_attributes(
            700123,
            [Attribute(attributeID=205, values=["A1"])],
            log_history=False,
        )

    request = next(r for r in fake_ips.requests if r.path == SET_ATTRS_URL)
    # Тело — голый JSON-массив AttributeDto.
    assert isinstance(request.body, list)
    assert request.body[0]["attributeID"] == 205
    assert request.body[0]["values"] == ["A1"]
    # result разворачивается в list[Attribute].
    assert result[0].attribute_id == 205
    assert result[0].values == ["A1"]


async def test_relation_set_attributes_empty_result(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", SET_ATTRS_URL, body={"result": None, "modificationsHistory": None})
    async with IPSClient(config=token_config) as ips:
        result = await ips.relation_set_attributes(700123, [], log_history=True)

    # Пустой список атрибутов на входе и result=null на выходе.
    request = next(r for r in fake_ips.requests if r.path == SET_ATTRS_URL)
    assert request.body == []
    assert result == []


async def test_relation_set_attribute_values_builds_body(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "post",
        SET_VALUES_URL,
        body={"result": [{"attributeId": 205, "values": ["A1"]}], "modificationsHistory": None},
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.relation_set_attribute_values(
            700123,
            [AttributeValues(attributeId=205, values=["A1"])],
            delete_not_existing=True,
            dont_delete_blobs=True,
            return_delta=True,
            modes=["includeName"],
        )

    request = next(r for r in fake_ips.requests if r.path == SET_VALUES_URL)
    body = request.body
    assert isinstance(body, dict)
    assert body["attributeValues"][0]["attributeId"] == 205
    assert body["attributeValues"][0]["values"] == ["A1"]
    assert body["deleteNotExistingAttribute"] is True
    assert body["dontDeleteBlobs"] is True
    assert body["returnDelta"] is True
    assert body["modes"] == ["includeName"]
    # result разворачивается в list[AttributeValues].
    assert result[0].attribute_id == 205


async def test_relation_set_attribute_values_defaults(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", SET_VALUES_URL, body={"result": None, "modificationsHistory": None})
    async with IPSClient(config=token_config) as ips:
        result = await ips.relation_set_attribute_values(
            700123,
            [AttributeValues(attributeId=205, values=["A1"])],
        )

    request = next(r for r in fake_ips.requests if r.path == SET_VALUES_URL)
    body = request.body
    assert body["deleteNotExistingAttribute"] is False
    assert body["dontDeleteBlobs"] is False
    assert body["returnDelta"] is False
    assert body["modes"] == []
    # result=null -> пустой список.
    assert result == []


async def test_relation_add_temporary_attribute_builds_body(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", TEMP_ATTR_URL, body={"attributeID": 205, "values": ["A1"]})
    async with IPSClient(config=token_config) as ips:
        attr = await ips.relation_add_temporary_attribute(
            700123,
            attribute_id=205,
            fail_if_exists=True,
            values=["A1"],
        )

    request = next(r for r in fake_ips.requests if r.path == TEMP_ATTR_URL)
    body = request.body
    assert isinstance(body, dict)
    assert body["attributeId"] == 205
    assert body["failIfExists"] is True
    assert body["values"] == ["A1"]
    # Ответ — одиночный AttributeDto -> Attribute.
    assert attr.attribute_id == 205
    assert attr.values == ["A1"]


async def test_relation_add_temporary_attribute_defaults(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", TEMP_ATTR_URL, body={"attributeID": 205, "values": []})
    async with IPSClient(config=token_config) as ips:
        await ips.relation_add_temporary_attribute(700123, attribute_id=205)

    request = next(r for r in fake_ips.requests if r.path == TEMP_ATTR_URL)
    body = request.body
    assert body["failIfExists"] is False
    assert body["values"] == []
