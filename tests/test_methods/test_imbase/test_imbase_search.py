"""Тесты методов поиска справочной системы IMBASE (чтение через POST)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.imbase.index_search_params import ImBaseIndexSearchParams
from aioips.schemas.imbase.table_search_params import ImBaseTableSearchParams

_Client = IPSClient


async def test_imbase_find_in_tables_posts_body_and_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    body = [
        {"linkId": 10, "recordIds": [1, 2, 3]},
        {"linkId": 11, "recordIds": [4]},
    ]
    fake_ips.add("post", "/core/api/imbase/find/inTables", body=body)
    params = ImBaseTableSearchParams(
        table_links_lookup={"204": [1, 2, 3]},
        conditions=[{"attributeId": 1029, "condition": "eq", "data": "Сталь"}],
    )
    async with _Client(config=token_config) as ips:
        result = await ips.imbase_find_in_tables(params)

    assert result == body
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/imbase/find/inTables"
    assert request.body == {
        "tableLinksLookup": {"204": [1, 2, 3]},
        "conditions": [{"attributeId": 1029, "condition": "eq", "data": "Сталь"}],
    }


async def test_imbase_find_in_tables_filters_non_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/imbase/find/inTables", body=[{"linkId": 1}, 42, None])
    async with _Client(config=token_config) as ips:
        result = await ips.imbase_find_in_tables(ImBaseTableSearchParams())

    assert result == [{"linkId": 1}]


async def test_imbase_find_in_tables_non_list_returns_empty(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/imbase/find/inTables", body={"entity": None})
    async with _Client(config=token_config) as ips:
        result = await ips.imbase_find_in_tables(ImBaseTableSearchParams())

    assert result == []


async def test_imbase_find_by_index_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    entity = [{"objectId": 50}, {"objectId": 51}]
    fake_ips.add(
        "post",
        "/core/api/imbase/find/byIndex",
        body={"entity": entity, "isEntityPresent": True},
    )
    params = ImBaseIndexSearchParams(
        attribute_id=1029,
        search_query="550.07",
        search_accuracy="start",
        catalog_ids=[12, 34],
        result_count_limit=50,
    )
    async with _Client(config=token_config) as ips:
        result = await ips.imbase_find_by_index(params)

    assert result == entity
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/imbase/find/byIndex"
    assert request.body == {
        "attributeId": 1029,
        "searchQuery": "550.07",
        "searchAccuracy": "start",
        "catalogIds": [12, 34],
        "resultCountLimit": 50,
    }


async def test_imbase_find_by_index_null_entity_returns_empty(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "post",
        "/core/api/imbase/find/byIndex",
        body={"entity": None, "isEntityPresent": False},
    )
    async with _Client(config=token_config) as ips:
        result = await ips.imbase_find_by_index(ImBaseIndexSearchParams(attribute_id=1))

    assert result == []


async def test_imbase_attribute_existing_values_returns_dict(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    guid = "8f3c2a10-0000-0000-0000-000000000000"
    body = {"values": ["Сталь", "Алюминий"], "linkValuesNames": {"5": "Латунь"}}
    fake_ips.add(
        "post",
        f"/core/api/imbase/attribute/byGuid/{guid}/existingValues",
        body=body,
    )
    params = ImBaseTableSearchParams(table_links_lookup={"204": [1, 2]})
    async with _Client(config=token_config) as ips:
        result = await ips.imbase_attribute_existing_values(guid, params)

    assert result == body
    request = fake_ips.requests[-1]
    assert request.path == f"/core/api/imbase/attribute/byGuid/{guid}/existingValues"
    assert request.body == {"tableLinksLookup": {"204": [1, 2]}, "conditions": []}


async def test_imbase_attribute_existing_values_coerces_non_dict(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    guid = "abc"
    fake_ips.add(
        "post",
        f"/core/api/imbase/attribute/byGuid/{guid}/existingValues",
        body=[1, 2, 3],
    )
    async with _Client(config=token_config) as ips:
        result = await ips.imbase_attribute_existing_values(guid, ImBaseTableSearchParams())

    assert result == {}
