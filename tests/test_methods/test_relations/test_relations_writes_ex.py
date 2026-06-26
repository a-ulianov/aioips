"""Тесты расширенных write-методов связей: attributeValuesEx и пакетное обновление."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.objects import AttributeValues, SetAttributeValuesExBody


async def test_relation_set_attribute_values_ex_unwraps_dict(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "post",
        "/core/api/relations/700123/attributeValuesEx",
        body={"result": {"205": {"message": "ok"}}, "modificationsHistory": []},
    )
    async with IPSClient(config=token_config) as ips:
        errors = await ips.relation_set_attribute_values_ex(
            700123,
            SetAttributeValuesExBody(
                attribute_values=[AttributeValues(attribute_id=205, values=["A1"])],
                return_delta=True,
            ),
        )
    assert errors == {"205": {"message": "ok"}}
    req = next(r for r in fake_ips.requests if "attributeValuesEx" in r.path)
    assert req.body["returnDelta"] is True
    assert req.body["attributeValues"][0]["attributeId"] == 205
    assert req.query["isNeedToLogModificationHistory"] == "true"


async def test_relation_set_attribute_values_ex_empty_result(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "post",
        "/core/api/relations/700123/attributeValuesEx",
        body={"result": None, "modificationsHistory": []},
    )
    async with IPSClient(config=token_config) as ips:
        errors = await ips.relation_set_attribute_values_ex(
            700123, SetAttributeValuesExBody(), log_history=False
        )
    assert errors == {}
    req = next(r for r in fake_ips.requests if "attributeValuesEx" in r.path)
    assert req.query["isNeedToLogModificationHistory"] == "false"


async def test_relation_update_relations_attributes_unwraps_dict(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "post",
        "/core/api/relations/attributes",
        body={"result": {"relationIds": [700123, 700124]}, "modificationsHistory": []},
    )
    payload = {
        "relationsAttributes": [
            {"relationId": 700123, "attributes": [{"attributeId": 205, "values": ["A1"]}]},
        ]
    }
    async with IPSClient(config=token_config) as ips:
        result = await ips.relation_update_relations_attributes(payload)
    assert result["relationIds"] == [700123, 700124]
    req = next(r for r in fake_ips.requests if r.path == "/core/api/relations/attributes")
    # Тело передаётся как есть.
    assert req.body == payload
    assert req.query["isNeedToLogModificationHistory"] == "true"
