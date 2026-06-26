"""Тесты методов чтения объектов."""

from uuid import UUID

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.common.enumerations import ObjectModifyMode

_OBJECT = {
    "objectID": 102550,
    "id": 5005,
    "versionID": 1,
    "objectType": 1127,
    "caption": "Деталь А",
    "guid": "cad001c5-306c-11d8-b4e9-00304f19f545",
    "objectGUID": "cad001c5-306c-11d8-b4e9-00304f19f546",
    "isBaseVersion": True,
    "objectModifyMode": "checkout",
    "filtrationState": "fsNotRequired",
}
_INFO = {
    "id": 5005,
    "objectID": 102550,
    "objectTypeID": 1127,
    "versionGuid": "cad001c5-306c-11d8-b4e9-00304f19f545",
    "caption": "Деталь А",
}


async def test_object_get_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/objects/102550",
        body={"entity": _OBJECT, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        obj = await ips.object_get(102550)

    assert obj is not None
    assert obj.object_id == 102550
    assert obj.caption == "Деталь А"
    assert obj.object_modify_mode == ObjectModifyMode.CHECKOUT
    assert obj.guid == UUID("cad001c5-306c-11d8-b4e9-00304f19f545")


async def test_object_get_returns_none_when_absent(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/objects/999",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        obj = await ips.object_get(999)

    assert obj is None


async def test_object_get_by_guid(token_config: IPSConfig, fake_ips: FakeIPS):
    guid = "cad001c5-306c-11d8-b4e9-00304f19f545"
    fake_ips.add(
        "get",
        f"/core/api/objects/byGuid/{guid}",
        body={"entity": _OBJECT, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        obj = await ips.object_get_by_guid(guid)

    assert obj is not None
    assert obj.id == 5005


async def test_objects_collection_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/objects/collection", body=[_OBJECT, _OBJECT])
    async with IPSClient(config=token_config) as ips:
        objects = await ips.objects_collection([102550, 102551])

    assert len(objects) == 2
    assert all(o.object_id == 102550 for o in objects)


async def test_objects_collection_sends_ids_in_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/objects/collection", body=[])
    async with IPSClient(config=token_config) as ips:
        await ips.objects_collection([1, 2, 3])

    request = next(r for r in fake_ips.requests if r.path == "/core/api/objects/collection")
    assert request.body == [1, 2, 3]


async def test_object_info(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/objects/102550/objectInfo",
        body={"entity": _INFO, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        info = await ips.object_info(102550)

    assert info is not None
    assert info.object_type_id == 1127
    assert info.caption == "Деталь А"


async def test_object_info_by_guid_absent_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    guid = "cad001c5-306c-11d8-b4e9-00304f19f545"
    fake_ips.add(
        "get",
        f"/core/api/objects/byGuid/{guid}/objectInfo",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        info = await ips.object_info_by_guid(guid)

    assert info is None
