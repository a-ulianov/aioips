"""Тесты read-методов табличных частей и связей справочной системы IMBASE."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

ImBaseClient = IPSClient


async def test_imbase_table_data_returns_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {"columns": [{"id": 1, "name": "Марка"}], "rows": [{"id": 10}]}
    fake_ips.add("get", "/core/api/imbase/table/7", body=body)
    async with ImBaseClient(config=token_config) as ips:
        table = await ips.imbase_table_data(7)

    assert table == body
    assert fake_ips.requests[-1].path == "/core/api/imbase/table/7"


async def test_imbase_table_data_coerces_non_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/imbase/table/7", body=[1, 2, 3])
    async with ImBaseClient(config=token_config) as ips:
        table = await ips.imbase_table_data(7)

    assert table == {}


async def test_imbase_table_display_settings_returns_dict(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    body = {"columns": [{"id": 1, "visible": True}]}
    fake_ips.add("get", "/core/api/imbase/table/7/displaySettings", body=body)
    async with ImBaseClient(config=token_config) as ips:
        settings = await ips.imbase_table_display_settings(7)

    assert settings == body


async def test_imbase_table_user_filter_returns_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {"conditions": [{"attributeId": 1029, "op": "eq"}]}
    fake_ips.add("get", "/core/api/imbase/table/7/userFilter", body=body)
    async with ImBaseClient(config=token_config) as ips:
        user_filter = await ips.imbase_table_user_filter(7)

    assert user_filter == body


async def test_imbase_table_created_objects_unwraps_entity(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    entity = {"1001": [{"objectId": 50, "objectVersionId": 7}]}
    fake_ips.add(
        "get",
        "/core/api/imbase/table/7/createdObjects",
        body={"entity": entity, "isEntityPresent": True},
    )
    async with ImBaseClient(config=token_config) as ips:
        created = await ips.imbase_table_created_objects(7)

    assert created == entity


async def test_imbase_table_created_objects_null_entity_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/imbase/table/7/createdObjects",
        body={"entity": None, "isEntityPresent": False},
    )
    async with ImBaseClient(config=token_config) as ips:
        created = await ips.imbase_table_created_objects(7)

    assert created is None


async def test_imbase_table_record_mix_usage_unwraps_entity(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    entity = {"tableMixes": [{"id": 9, "name": "Состав"}]}
    fake_ips.add(
        "get",
        "/core/api/imbase/table/204/records/1001/tableMixUsage",
        body={"entity": entity, "isEntityPresent": True},
    )
    async with ImBaseClient(config=token_config) as ips:
        usage = await ips.imbase_table_record_mix_usage(204, 1001)

    assert usage == entity


async def test_imbase_table_record_mix_usage_null_entity_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/imbase/table/204/records/1001/tableMixUsage",
        body={"entity": None, "isEntityPresent": False},
    )
    async with ImBaseClient(config=token_config) as ips:
        usage = await ips.imbase_table_record_mix_usage(204, 1001)

    assert usage is None


async def test_imbase_table_check_composition_returns_dict(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    body = {"possible": True, "reasons": []}
    fake_ips.add("get", "/core/api/imbase/table/204/checkComposition/1742", body=body)
    async with ImBaseClient(config=token_config) as ips:
        result = await ips.imbase_table_check_composition(204, 1742)

    assert result == body
    assert fake_ips.requests[-1].path == "/core/api/imbase/table/204/checkComposition/1742"


async def test_imbase_table_search_links_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    entity = [{"linkId": 1, "name": "Поиск"}, {"linkId": 2, "name": "Поиск2"}]
    fake_ips.add(
        "get",
        "/core/api/imbase/links/byParent/102550",
        body={"entity": entity, "isEntityPresent": True},
    )
    async with ImBaseClient(config=token_config) as ips:
        links = await ips.imbase_table_search_links(102550)

    assert links == entity


async def test_imbase_table_search_links_null_entity_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/imbase/links/byParent/102550",
        body={"entity": None, "isEntityPresent": False},
    )
    async with ImBaseClient(config=token_config) as ips:
        links = await ips.imbase_table_search_links(102550)

    assert links is None


async def test_imbase_object_linked_table_record_attributes_unwraps_entity(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    entity = [
        {
            "attributeId": 1029,
            "attributeName": "Архив",
            "attributeGuid": "cad001c5-306c-11d8-b4e9-00304f19f545",
            "attributeAlias": "ARCH",
            "attributeType": "ftObjectLink",
            "values": [777],
        }
    ]
    fake_ips.add(
        "get",
        "/core/api/imbase/object/102550/linkedImBaseTableRecord/attributes",
        body={"entity": entity, "isEntityPresent": True},
    )
    async with ImBaseClient(config=token_config) as ips:
        attrs = await ips.imbase_object_linked_table_record_attributes(102550)

    assert attrs is not None
    assert attrs[0].attribute_id == 1029
    assert attrs[0].attribute_name == "Архив"
    assert attrs[0].values == [777]


async def test_imbase_object_linked_table_record_attributes_null_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/imbase/object/102550/linkedImBaseTableRecord/attributes",
        body={"entity": None, "isEntityPresent": False},
    )
    async with ImBaseClient(config=token_config) as ips:
        attrs = await ips.imbase_object_linked_table_record_attributes(102550)

    assert attrs is None
