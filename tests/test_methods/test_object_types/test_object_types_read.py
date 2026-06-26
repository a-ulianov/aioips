"""Тесты методов чтения раздела типов объектов (контроллер ``objectTypes``)."""

from uuid import UUID

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_TYPE_GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"

_DEFINITION = {
    "objectType": 1742,
    "objectTypeGuid": _TYPE_GUID,
    "objectTypeName": "Деталь",
    "objectTypeShortName": "Дет",
    "objectInstanceName": "деталь",
    "areaID": "main",
    "anyAttributes": False,
    "publicLCSchema": "private",
    "changeObjectsSchema": True,
    "versionable": "multiVersion",
    "note": "комментарий",
    "defaultRelation": 7,
    "parentTypeID": 100,
    "captionAttribute": 55,
    "lifetimeReserve": 30,
    "options": ["notificationsEnabled", "createSnapshots"],
    "schemaID": 12,
    "isLocalType": False,
    "classifiedOption": 0,
}

_QUICK_INFO = {"id": 1742, "guid": _TYPE_GUID, "name": "Деталь"}

_QUICK_OBJECT = {
    "id": 9001,
    "objectID": 8001,
    "objectTypeID": 1742,
    "versionGuid": _TYPE_GUID,
    "caption": "Деталь №1",
}


async def test_object_type_object_ids_returns_ints(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/objectTypes/1742/objectIds", body=[8001, 8002, 8003])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.object_type_object_ids(1742)

    assert ids == [8001, 8002, 8003]


async def test_object_type_objects_returns_quick_info(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/objectTypes/1742/objects", body=[_QUICK_OBJECT])
    async with IPSClient(config=token_config) as ips:
        items = await ips.object_type_objects(1742)

    assert len(items) == 1
    assert items[0].id == 9001
    assert items[0].object_id == 8001
    assert items[0].object_type_id == 1742
    assert items[0].caption == "Деталь №1"


async def test_object_type_objects_info_unwrapped(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {"objectType": 1742, "objectsCount": 12, "snapshotsCount": 34}
    fake_ips.add("get", "/core/api/objectTypes/1742/objectsInfo", body=body)
    async with IPSClient(config=token_config) as ips:
        info = await ips.object_type_objects_info(1742)

    assert info.object_type == 1742
    assert info.objects_count == 12
    assert info.snapshots_count == 34


async def test_object_type_definition_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/objectTypes/1742",
        body={"entity": _DEFINITION, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        definition = await ips.object_type_definition(1742)

    assert definition is not None
    assert definition.object_type == 1742
    assert definition.object_type_guid == UUID(_TYPE_GUID)
    assert definition.object_type_name == "Деталь"
    assert definition.parent_type_id == 100
    assert definition.schema_id == 12
    assert definition.public_lc_schema == "private"
    assert definition.versionable == "multiVersion"
    assert definition.options == ["notificationsEnabled", "createSnapshots"]


async def test_object_type_definition_absent_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/objectTypes/9999",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        definition = await ips.object_type_definition(9999)

    assert definition is None


async def test_object_type_definition_coerces_null_options(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    body = {"entity": {**_DEFINITION, "options": None}, "isEntityPresent": True}
    fake_ips.add("get", "/core/api/objectTypes/1742", body=body)
    async with IPSClient(config=token_config) as ips:
        definition = await ips.object_type_definition(1742)

    assert definition is not None
    assert definition.options == []


async def test_object_type_definition_by_guid_unwraps(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/objectTypes/byGuid/{_TYPE_GUID}",
        body={"entity": _DEFINITION, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        definition = await ips.object_type_definition_by_guid(_TYPE_GUID)

    assert definition is not None
    assert definition.object_type == 1742


async def test_object_type_definition_by_name_encodes_path(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    # aiohttp декодирует путь до матчинга, поэтому регистрируем читаемый путь.
    fake_ips.add(
        "get",
        "/core/api/objectTypes/byName/Деталь сборная",
        body={"entity": _DEFINITION, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        definition = await ips.object_type_definition_by_name("Деталь сборная")

    assert definition is not None
    assert definition.object_type == 1742
    # пробел кодируется как %20, а не "+"
    assert "%20" in fake_ips.requests[-1].path or "Деталь" in fake_ips.requests[-1].path


async def test_object_type_quick_info_unwraps(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/objectTypes/1742/objectTypeInfo",
        body={"entity": _QUICK_INFO, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        info = await ips.object_type_quick_info(1742)

    assert info is not None
    assert info.id == 1742
    assert info.guid == UUID(_TYPE_GUID)
    assert info.name == "Деталь"


async def test_object_type_quick_info_absent_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/objectTypes/9999/objectTypeInfo",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        info = await ips.object_type_quick_info(9999)

    assert info is None


async def test_object_type_quick_info_by_guid_unwraps(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/objectTypes/byGuid/{_TYPE_GUID}/objectTypeInfo",
        body={"entity": _QUICK_INFO, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        info = await ips.object_type_quick_info_by_guid(_TYPE_GUID)

    assert info is not None
    assert info.id == 1742


async def test_object_type_all_child_guids_returns_strings(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    guids = [_TYPE_GUID, "cad001c5-306c-11d8-b4e9-00304f19f546"]
    fake_ips.add(
        "get",
        f"/core/api/objectTypes/byGuid/{_TYPE_GUID}/allChildGuids",
        body=guids,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_type_all_child_guids(_TYPE_GUID)

    assert result == guids
