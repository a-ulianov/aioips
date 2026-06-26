"""Тесты legacy search-методов раздела связей (контроллер ``Relations`` с заглавной)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.relations.relation_collection_request import RelationCollectionRequest

_Client = IPSClient

CONSIST_FROM_URL = "/core/api/Relations/ConsistFromRequest"
ENTERS_IN_URL = "/core/api/Relations/EntersInVersionRequest"

_EDGE = {
    "relationTypeId": 2,
    "parentObjectId": 102550,
    "parentObjectTypeId": 1742,
    "objectId": 200300,
    "objectGuid": "00000000-0000-0000-0000-000000000001",
    "objectTypeId": 1743,
    "partId": 999,
}


async def test_relations_consist_from_request_parses_and_builds(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", CONSIST_FROM_URL, body=[_EDGE])
    async with _Client(config=token_config) as ips:
        edges = await ips.relations_consist_from_request(
            RelationCollectionRequest(object_id=102550, is_recure=True, relation_type_id=2)
        )

    assert len(edges) == 1
    edge = edges[0]
    assert edge.parent_object_id == 102550
    assert edge.object_id == 200300  # id ОБЪЕКТА
    assert edge.part_id == 999  # id ВЕРСИИ дочернего (≠ object_id)

    request = next(r for r in fake_ips.requests if r.path == CONSIST_FROM_URL)
    assert request.method == "POST"
    assert request.body["objectId"] == 102550
    assert request.body["isRecure"] is True
    assert request.body["relationTypeID"] == 2  # заглавный акроним-алиас


async def test_relations_enters_in_version_request_parses_and_builds(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", ENTERS_IN_URL, body=[_EDGE])
    async with _Client(config=token_config) as ips:
        edges = await ips.relations_enters_in_version_request(
            RelationCollectionRequest(object_id=102550)
        )

    assert edges[0].parent_object_id == 102550
    request = next(r for r in fake_ips.requests if r.path == ENTERS_IN_URL)
    assert request.method == "POST"
    assert request.body["objectId"] == 102550
    # дефолты: любой тип связи/объекта
    assert request.body["relationTypeID"] == -1
    assert request.body["objectTypeID"] == -1


async def test_relations_request_empty_result(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", CONSIST_FROM_URL, body=[])
    async with _Client(config=token_config) as ips:
        edges = await ips.relations_consist_from_request(RelationCollectionRequest(object_id=1))
    assert edges == []
