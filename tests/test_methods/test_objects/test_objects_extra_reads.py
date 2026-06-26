"""Тесты дополнительных читающих GET-методов раздела объектов.

Проверяют путь, query и распаковку ответа для одиннадцати методов: скаляры
(``object_checkout_date``, ``object_hash_version``, ``object_is_parent_type``,
``object_check_visibility_available``), unwrap entity (``object_by_version_rule`` и
``*_by_guid``, ``object_attribute_values_by_guid``), void
(``object_check_relations_edit``), объект-схему (``object_snapshot_info``) и голые
массивы (``object_snapshot_readonly_objects``, ``object_visibilities``). Внешний HTTP
мокируется ``FakeIPS``.
"""

from urllib.parse import quote

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

OBJ = 102550
GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"
TYPE_GUID = "11111111-2222-3333-4444-555555555555"


async def test_checkout_date_returns_string(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/objects/{OBJ}/getCheckOutDate"
    fake_ips.add("get", path, body="2026-06-25T10:00:00Z")
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_checkout_date(OBJ)
    assert result == "2026-06-25T10:00:00Z"
    assert any(r.path == path and r.method == "GET" for r in fake_ips.requests)


async def test_hash_version_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/objects/{OBJ}/getHashVersion"
    fake_ips.add("get", path, body=123456789)
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_hash_version(OBJ)
    assert result == 123456789
    assert isinstance(result, int)


async def test_is_parent_type_passes_query_and_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = f"/core/api/objects/{OBJ}/isParentType"
    fake_ips.add("get", path, body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_is_parent_type(OBJ, TYPE_GUID)
    assert result is True
    request = next(r for r in fake_ips.requests if r.path == path)
    assert request.query["objectTypeGuid"] == TYPE_GUID


async def test_by_version_rule_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/objects/{OBJ}/objectByVersionRule"
    fake_ips.add(
        "get", path, body={"entity": {"objectID": OBJ, "id": 9001}, "isEntityPresent": True}
    )
    async with IPSClient(config=token_config) as ips:
        obj = await ips.object_by_version_rule(OBJ)
    assert obj is not None
    assert obj.object_id == OBJ
    assert obj.id == 9001


async def test_by_version_rule_none_when_entity_absent(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/objects/{OBJ}/objectByVersionRule"
    fake_ips.add("get", path, body={"entity": None, "isEntityPresent": False})
    async with IPSClient(config=token_config) as ips:
        obj = await ips.object_by_version_rule(OBJ)
    assert obj is None


async def test_by_version_rule_by_guid_unwraps_and_encodes(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    encoded = quote(GUID, safe="")
    path = f"/core/api/objects/byGuid/{encoded}/objectByVersionRule"
    fake_ips.add("get", path, body={"entity": {"objectID": OBJ, "id": 9002}})
    async with IPSClient(config=token_config) as ips:
        obj = await ips.object_by_version_rule_by_guid(GUID)
    assert obj is not None
    assert obj.id == 9002
    assert any(r.path == path for r in fake_ips.requests)


async def test_check_relations_edit_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/objects/{OBJ}/checkRelationsEdit"
    fake_ips.add("get", path, body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_check_relations_edit(OBJ)
    assert result is None
    assert any(r.path == path and r.method == "GET" for r in fake_ips.requests)


async def test_attribute_values_by_guid_unwraps_array(token_config: IPSConfig, fake_ips: FakeIPS):
    encoded = quote(GUID, safe="")
    path = f"/core/api/objects/{encoded}/attributes/12/by-guid/values"
    fake_ips.add("get", path, body={"entity": ["a", "b"], "isEntityPresent": True})
    async with IPSClient(config=token_config) as ips:
        values = await ips.object_attribute_values_by_guid(GUID, 12)
    assert values == ["a", "b"]


async def test_attribute_values_by_guid_none_when_entity_null(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    encoded = quote(GUID, safe="")
    path = f"/core/api/objects/{encoded}/attributes/12/by-guid/values"
    fake_ips.add("get", path, body={"entity": None, "isEntityPresent": False})
    async with IPSClient(config=token_config) as ips:
        values = await ips.object_attribute_values_by_guid(GUID, 12)
    assert values is None


async def test_snapshot_info_parses_schema(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/objects/{OBJ}/snapshots/info"
    fake_ips.add(
        "get",
        path,
        body={
            "activeSnapshotId": 7,
            "objectSnapshotCollection": [
                {"snapshotId": 7, "name": "snap-A"},
                {"snapshotId": 8, "name": None},
            ],
        },
    )
    async with IPSClient(config=token_config) as ips:
        info = await ips.object_snapshot_info(OBJ)
    assert info.active_snapshot_id == 7
    assert [s.snapshot_id for s in info.object_snapshot_collection] == [7, 8]
    assert info.object_snapshot_collection[0].name == "snap-A"


async def test_snapshot_info_null_collection_becomes_empty(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = f"/core/api/objects/{OBJ}/snapshots/info"
    fake_ips.add("get", path, body={"activeSnapshotId": None, "objectSnapshotCollection": None})
    async with IPSClient(config=token_config) as ips:
        info = await ips.object_snapshot_info(OBJ)
    assert info.active_snapshot_id is None
    assert info.object_snapshot_collection == []  # null -> []


async def test_snapshot_readonly_objects_returns_int_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = f"/core/api/objects/{OBJ}/snapshots/7/info"
    fake_ips.add("get", path, body=[200, 201, 202])
    async with IPSClient(config=token_config) as ips:
        ro = await ips.object_snapshot_readonly_objects(OBJ, 7)
    assert ro == [200, 201, 202]


async def test_visibilities_parses_array(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/objects/{OBJ}/visibilities"
    fake_ips.add(
        "get",
        path,
        body=[
            {"objectId": 200, "objectType": 5, "objectName": "node", "isVisible": True},
        ],
    )
    async with IPSClient(config=token_config) as ips:
        settings = await ips.object_visibilities(OBJ)
    assert len(settings) == 1
    assert settings[0].object_name == "node"
    assert settings[0].is_visible is True


async def test_check_visibility_available_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/objects/{OBJ}/visibilities/checkVisibilityAvailable"
    fake_ips.add("get", path, body=False)
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_check_visibility_available(OBJ)
    assert result is False
