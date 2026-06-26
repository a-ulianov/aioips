"""Тесты методов чтения раздела запросов состава/вхождения (``/core/api/Relations``)."""

from uuid import UUID

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_RELATION = {
    "relationTypeId": 7,
    "parentObjectId": 102550,
    "parentObjectTypeId": 31,
    "objectId": 102560,
    "objectGuid": "cad001c5-306c-11d8-b4e9-00304f19f545",
    "objectTypeId": 32,
    "partId": 200300,
}

_RELATION_TYPE = {
    "id": 7,
    "guid": "cad001c5-306c-11d8-b4e9-00304f19f546",
    "description": "Состоит из",
    "name": "Состав",
    "reverseName": "Входит в",
    "note": "примечание",
}


async def test_consist_from_returns_relations(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Relations/ConsistFrom", body=[_RELATION, _RELATION])
    async with IPSClient(config=token_config) as ips:
        relations = await ips.consist_from(102550)

    assert len(relations) == 2
    rel = relations[0]
    assert rel.relation_type_id == 7
    assert rel.parent_object_id == 102550
    assert rel.parent_object_type_id == 31
    assert rel.object_id == 102560
    assert rel.object_guid == UUID("cad001c5-306c-11d8-b4e9-00304f19f545")
    assert rel.object_type_id == 32
    assert rel.part_id == 200300

    captured = fake_ips.requests[-1]
    assert captured.query["objectId"] == "102550"
    assert "recure" not in captured.query


async def test_consist_from_passes_optional_query_flags(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Relations/ConsistFrom", body=[])
    async with IPSClient(config=token_config) as ips:
        await ips.consist_from(102550, recure=True, relation_type_id=7, object_type_id=32)

    query = fake_ips.requests[-1].query
    assert query["objectId"] == "102550"
    assert query["recure"] == "true"
    assert query["relationTypeId"] == "7"
    assert query["objectTypeId"] == "32"


async def test_consist_from_recure_false_serialized_lowercase(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/Relations/ConsistFrom", body=[])
    async with IPSClient(config=token_config) as ips:
        await ips.consist_from(102550, recure=False)

    assert fake_ips.requests[-1].query["recure"] == "false"


async def test_enters_in_version_returns_relations(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Relations/EntersInVersion", body=[_RELATION])
    async with IPSClient(config=token_config) as ips:
        relations = await ips.enters_in_version(102560)

    assert len(relations) == 1
    assert relations[0].parent_object_id == 102550
    assert relations[0].part_id == 200300

    query = fake_ips.requests[-1].query
    assert query["objectId"] == "102560"
    assert "recure" not in query
    assert "relationTypeId" not in query


async def test_enters_in_version_passes_optional_query_flags(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/Relations/EntersInVersion", body=[])
    async with IPSClient(config=token_config) as ips:
        await ips.enters_in_version(102560, recure=True, relation_type_id=7)

    query = fake_ips.requests[-1].query
    assert query["recure"] == "true"
    assert query["relationTypeId"] == "7"


async def test_relation_queries_relation_types_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/Relations/GetRelationTypes", body=[_RELATION_TYPE])
    async with IPSClient(config=token_config) as ips:
        types = await ips.relation_queries_relation_types()

    assert len(types) == 1
    rtype = types[0]
    assert rtype.id == 7
    assert rtype.guid == UUID("cad001c5-306c-11d8-b4e9-00304f19f546")
    assert rtype.name == "Состав"
    assert rtype.reverse_name == "Входит в"
    assert rtype.note == "примечание"


async def test_classifier_objects_returns_ints(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Relations/GetClassifierObjects", body=[101, 202, 303])
    async with IPSClient(config=token_config) as ips:
        result = await ips.classifier_objects(classifier_object_id=4200)

    assert result == [101, 202, 303]
    assert fake_ips.requests[-1].query["classifierObjectId"] == "4200"


async def test_classifier_objects_omits_query_when_not_set(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/Relations/GetClassifierObjects", body=[])
    async with IPSClient(config=token_config) as ips:
        result = await ips.classifier_objects()

    assert result == []
    assert "classifierObjectId" not in fake_ips.requests[-1].query
