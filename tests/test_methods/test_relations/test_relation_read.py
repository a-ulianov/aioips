"""Тесты методов чтения связей и их типов."""

from uuid import UUID

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_RELATION = {
    "relationID": 700123,
    "projID": 5005,
    "partID": 102550,
    "partObjectID": 6006,
    "relationType": 1,
    "creatorID": 42,
    "createDate": "2026-06-24T10:00:00Z",
    "filtrationOwnerID": None,
    "guid": "cad001c5-306c-11d8-b4e9-00304f19f545",
    "readOnly": False,
}
_RELATION_TYPE = {
    "id": 1,
    "guid": "cad001c5-306c-11d8-b4e9-00304f19f546",
    "description": "Состав изделия",
    "name": "Состоит из",
    "reverseName": "Входит в",
    "note": None,
}


async def test_relation_get_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/700123",
        body={"entity": _RELATION, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        relation = await ips.relation_get(700123)

    assert relation is not None
    assert relation.relation_id == 700123
    assert relation.proj_id == 5005
    assert relation.part_id == 102550
    assert relation.part_object_id == 6006
    assert relation.relation_type == 1
    assert relation.guid == UUID("cad001c5-306c-11d8-b4e9-00304f19f545")


async def test_relation_get_returns_none_when_absent(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/999",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        relation = await ips.relation_get(999)

    assert relation is None


async def test_relation_get_by_guid_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    guid = "cad001c5-306c-11d8-b4e9-00304f19f545"
    fake_ips.add(
        "get",
        f"/core/api/relations/byGuid/{guid}",
        body={"entity": _RELATION, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        relation = await ips.relation_get_by_guid(guid)

    assert relation is not None
    assert relation.proj_id == 5005
    assert relation.guid == UUID(guid)


async def test_relation_get_by_guid_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    guid = "cad001c5-306c-11d8-b4e9-00304f19f547"
    fake_ips.add(
        "get",
        f"/core/api/relations/byGuid/{guid}",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        relation = await ips.relation_get_by_guid(guid)

    assert relation is None


async def test_relations_by_project_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/projects/5005/relationTypes/1",
        body=[_RELATION, _RELATION],
    )
    async with IPSClient(config=token_config) as ips:
        relations = await ips.relations_by_project(5005, 1)

    assert len(relations) == 2
    assert all(r.proj_id == 5005 for r in relations)
    assert all(r.part_id == 102550 for r in relations)


async def test_relations_by_project_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/projects/5005/relationTypes/2",
        body=[],
    )
    async with IPSClient(config=token_config) as ips:
        relations = await ips.relations_by_project(5005, 2)

    assert relations == []


async def test_relation_types_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/Relations/GetRelationTypes",
        body=[_RELATION_TYPE],
    )
    async with IPSClient(config=token_config) as ips:
        types = await ips.relation_types()

    assert len(types) == 1
    assert types[0].id == 1
    assert types[0].name == "Состоит из"
    assert types[0].reverse_name == "Входит в"
    assert types[0].guid == UUID("cad001c5-306c-11d8-b4e9-00304f19f546")
