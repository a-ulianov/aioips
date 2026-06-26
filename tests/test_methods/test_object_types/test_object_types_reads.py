"""Тесты POST-методов ЧТЕНИЯ раздела типов объектов (иконки, дерево, состав)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.object_types.composition import ObjectsCompositionParams

_Client = IPSClient


async def test_object_type_icons_posts_ids_and_returns_map(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    body = {"1742": "aWNvbjE=", "1743": "aWNvbjI="}
    fake_ips.add("post", "/core/api/objectTypes/GetObjectTypeIcons", body=body)
    async with _Client(config=token_config) as ips:
        icons = await ips.object_type_icons([1742, 1743])

    assert icons == body
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/core/api/objectTypes/GetObjectTypeIcons"
    assert req.body == [1742, 1743]


async def test_object_type_icons_non_dict_returns_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/objectTypes/GetObjectTypeIcons", body=[1, 2])
    async with _Client(config=token_config) as ips:
        icons = await ips.object_type_icons([1742])

    assert icons == {}


async def test_object_types_tree_posts_ids_and_returns_dict(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    tree = {"root": 1742, "children": [1743, 1744]}
    fake_ips.add("post", "/core/api/objectTypes/GetObjectTypesTree", body=tree)
    async with _Client(config=token_config) as ips:
        result = await ips.object_types_tree([])

    assert result == tree
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/core/api/objectTypes/GetObjectTypesTree"
    assert req.body == []


async def test_object_types_tree_non_dict_returns_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/objectTypes/GetObjectTypesTree", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.object_types_tree([1742])

    assert result == {}


async def test_object_type_composition_with_model_params(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    item = {
        "objectID": 8001,
        "attributes": [{"attributeId": 55, "value": "Деталь №1"}],
        "objectCompositions": [{"object": {"objectID": 8002, "id": 9002}, "relation": {"id": 7}}],
    }
    fake_ips.add("post", "/core/api/objectTypes/1742/composition", body=[item])
    async with _Client(config=token_config) as ips:
        params = ObjectsCompositionParams(attribute_ids=[55])
        items = await ips.object_type_composition(1742, params)

    assert len(items) == 1
    assert items[0].object_id == 8001
    assert items[0].attributes[0]["attributeId"] == 55
    assert items[0].object_compositions[0]["object"]["objectID"] == 8002

    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/core/api/objectTypes/1742/composition"
    assert req.body == {"attributeIdsToSelect": [55]}


async def test_object_type_composition_none_params_sends_empty_body(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/objectTypes/1742/composition", body=[])
    async with _Client(config=token_config) as ips:
        items = await ips.object_type_composition(1742)

    assert items == []
    req = fake_ips.requests[-1]
    assert req.body == {}


async def test_object_type_composition_coerces_null_compositions(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    item = {"objectID": 8001, "attributes": None, "objectCompositions": None}
    fake_ips.add("post", "/core/api/objectTypes/1742/composition", body=[item])
    async with _Client(config=token_config) as ips:
        items = await ips.object_type_composition(1742, {"foo": "bar"})

    assert items[0].attributes == []
    assert items[0].object_compositions == []
    assert fake_ips.requests[-1].body == {"foo": "bar"}
