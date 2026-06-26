"""Тесты методов чтения раздела типов связей."""

from uuid import UUID

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_RELATION = {
    "relationID": 9001,
    "projID": 102550,
    "partID": 5005,
    "relationType": 1,
    "guid": "cad001c5-306c-11d8-b4e9-00304f19f545",
}


async def test_relation_type_relations_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relationTypes/1/relations",
        body=[_RELATION, _RELATION],
    )
    async with IPSClient(config=token_config) as ips:
        relations = await ips.relation_type_relations(1)

    assert len(relations) == 2
    relation = relations[0]
    assert relation.relation_id == 9001
    assert relation.proj_id == 102550
    assert relation.part_id == 5005
    assert relation.relation_type == 1
    assert relation.guid == UUID("cad001c5-306c-11d8-b4e9-00304f19f545")


async def test_relation_type_relations_requests_correct_path(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/relationTypes/42/relations", body=[])
    async with IPSClient(config=token_config) as ips:
        await ips.relation_type_relations(42)

    assert any(r.path == "/core/api/relationTypes/42/relations" for r in fake_ips.requests)


async def test_relation_type_relation_ids_returns_ints(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/relationTypes/1/relationIds", body=[9001, 9002, 9003])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.relation_type_relation_ids(1)

    assert ids == [9001, 9002, 9003]
