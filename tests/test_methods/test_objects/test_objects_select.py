"""Тесты метода поиска объектов."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.common.enumerations import ColumnContent, RelationalOperator
from aioips.schemas.objects import SelectCondition

SELECT_URL = "/core/api/objects/select"


async def test_objects_select_parses_results(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        SELECT_URL,
        body=[
            {
                "objectId": 1311983,
                "attributes": [
                    {"attributeId": 9, "value": ""},
                    {"attributeId": 10, "value": "ФЛГЦ-360П - Форма.jpg"},
                ],
            },
            {"objectId": 1288391, "attributes": None},
        ],
    )
    async with IPSClient(config=token_config) as ips:
        results = await ips.objects_select(
            object_type_id=1742,
            conditions=[
                SelectCondition(
                    attribute_id=1029,
                    relational_operator=RelationalOperator.EQUAL,
                    value=1240084,
                    content=ColumnContent.ID,
                )
            ],
            attribute_ids=[9, 10],
        )

    assert [r.object_id for r in results] == [1311983, 1288391]
    assert results[0].values[10] == "ФЛГЦ-360П - Форма.jpg"
    assert results[1].attributes == []  # null -> []


async def test_objects_select_builds_payload(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", SELECT_URL, body=[])
    async with IPSClient(config=token_config) as ips:
        await ips.objects_select(
            object_type_id=1742,
            conditions=[
                SelectCondition(
                    attribute_id=1029,
                    relational_operator=RelationalOperator.EQUAL,
                    value=1240084,
                    content=ColumnContent.ID,
                )
            ],
            attribute_ids=[9, 10],
            record_count=100,
        )

    request = next(r for r in fake_ips.requests if r.path == SELECT_URL)
    body = request.body
    assert body["objectTypeId"] == 1742
    assert body["attributeIdsToSelect"] == [9, 10]
    assert body["recordCount"] == 100
    cond = body["conditions"][0]
    assert cond["attributeId"] == 1029
    assert cond["relationalOperator"] == "equal"
    assert cond["content"] == "id"
    assert cond["groupID"] == 0  # uppercase alias
    assert cond["value"] == 1240084


async def test_objects_select_no_conditions(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", SELECT_URL, body=[])
    async with IPSClient(config=token_config) as ips:
        results = await ips.objects_select(object_type_id=1029)

    request = next(r for r in fake_ips.requests if r.path == SELECT_URL)
    assert request.body["conditions"] == []
    assert request.body["attributeIdsToSelect"] == []
    assert results == []
