"""Тесты читающих POST-методов раздела объектов (без мутаций).

Проверяют построение тела/пути/query и распаковку ответа для четырёх методов:
``objects_all_versions``, ``object_composition``, ``object_by_versions_rule``,
``object_calculated_attribute_values``. Внешний HTTP мокируется ``FakeIPS``.
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.objects import AllObjectVersionsParameters, AttributeValues

ALL_VERSIONS_URL = "/core/api/objects/allObjectVersions"
COMPOSITION_URL = "/core/api/objects/102550/composition"
RULE_URL = "/core/api/objects/102550/getObjectByVersionsRule/778"
CALC_URL = "/core/api/objects/102550/attributes/getCalculatedValues"


async def test_all_versions_parses_and_builds_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        ALL_VERSIONS_URL,
        body=[
            {"objectId": 102550, "attributes": [{"attributeId": 9, "value": "v1"}]},
            {"objectId": 102551, "attributes": None},
        ],
    )
    async with IPSClient(config=token_config) as ips:
        versions = await ips.objects_all_versions(
            AllObjectVersionsParameters(id=102550, is_object_id=True, attribute_ids=[9])
        )

    assert [v.object_id for v in versions] == [102550, 102551]
    assert versions[0].values[9] == "v1"
    assert versions[1].attributes == []  # null -> []

    request = next(r for r in fake_ips.requests if r.path == ALL_VERSIONS_URL)
    assert request.body["id"] == 102550
    assert request.body["isObjectId"] is True
    assert request.body["attributeIdsToSelect"] == [9]


async def test_composition_simple_unwraps_object_and_default_body(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "post",
        COMPOSITION_URL,
        body=[
            {"object": {"objectID": 200, "id": 201, "caption": "part"}, "relation": {}},
            {"relation": {}},  # без object — пропускается
        ],
    )
    async with IPSClient(config=token_config) as ips:
        parts = await ips.object_composition(102550)

    assert [p.object_id for p in parts] == [200]
    assert parts[0].caption == "part"

    request = next(r for r in fake_ips.requests if r.path == COMPOSITION_URL)
    # context_rule None -> exclude_none даёт пустое тело {}
    assert request.body == {}


async def test_composition_simple_passes_context_rule(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", COMPOSITION_URL, body=[])
    async with IPSClient(config=token_config) as ips:
        await ips.object_composition(102550, context_rule={"versionRuleObjectId": 778})

    request = next(r for r in fake_ips.requests if r.path == COMPOSITION_URL)
    assert request.body == {"contextRule": {"versionRuleObjectId": 778}}


async def test_by_versions_rule_parses_object_and_query(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        RULE_URL,
        body={"objectID": 102550, "id": 9001, "caption": "selected"},
    )
    async with IPSClient(config=token_config) as ips:
        obj = await ips.object_by_versions_rule(102550, 778, throw_not_found=True)

    assert obj.object_id == 102550
    assert obj.id == 9001
    assert obj.caption == "selected"

    request = next(r for r in fake_ips.requests if r.path == RULE_URL)
    assert request.body == {}  # тело {} чтобы избежать 415
    assert request.query["throwNotFoundException"] == "true"


async def test_by_versions_rule_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        RULE_URL,
        body={"entity": {"objectID": 102550, "id": 9001}},
    )
    async with IPSClient(config=token_config) as ips:
        obj = await ips.object_by_versions_rule(102550, 778)

    assert obj.object_id == 102550
    request = next(r for r in fake_ips.requests if r.path == RULE_URL)
    assert "throwNotFoundException" not in request.query  # None -> не передаётся


async def test_calculated_values_parses_and_builds_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        CALC_URL,
        body=[{"attributeId": 12, "values": ["550.07.305"]}],
    )
    async with IPSClient(config=token_config) as ips:
        calc = await ips.object_calculated_attribute_values(
            102550,
            [AttributeValues(attribute_id=12, values=["550.07.305"])],
            modes="all",
        )

    assert calc[0].attribute_id == 12
    assert calc[0].values == ["550.07.305"]

    request = next(r for r in fake_ips.requests if r.path == CALC_URL)
    assert isinstance(request.body, list)  # голый массив, не объект
    assert request.body[0]["attributeId"] == 12
    assert request.query["modes"] == "all"
