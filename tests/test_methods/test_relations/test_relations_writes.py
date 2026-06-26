"""Тесты мутирующих write-методов связей (create/createCollection/delete/deleteAttribute)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.objects import AttributeValues
from aioips.schemas.relations import CreateRelation

CREATE_URL = "/core/api/relations"
COLLECTION_URL = "/core/api/relations/collection"
DELETE_URL = "/core/api/relations"
DELETE_ATTR_URL = "/core/api/relations/700123/attributes/205"


async def test_relation_create_builds_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        CREATE_URL,
        body={
            "result": {"relationID": 700123, "projID": 102550, "partID": 102777, "relationType": 1},
            "modificationsHistory": None,
        },
    )
    async with IPSClient(config=token_config) as ips:
        rel = await ips.relation_create(
            CreateRelation(
                relation_type=1,
                proj_version_id=102550,
                part_version_id=102777,
                attribute_values=[AttributeValues(attributeId=205, values=["A1"])],
            ),
            log_history=False,
        )

    request = next(r for r in fake_ips.requests if r.path == CREATE_URL and r.method == "POST")
    body = request.body
    assert isinstance(body, dict)
    assert body["relationType"] == 1
    assert body["projVersionId"] == 102550
    assert body["partVersionId"] == 102777
    assert body["attributeValues"][0]["attributeId"] == 205
    assert request.query["isNeedToLogModificationHistory"] == "false"
    # result -> Relation.
    assert rel.relation_id == 700123
    assert rel.proj_id == 102550
    assert rel.part_id == 102777


async def test_relation_create_collection_builds_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        COLLECTION_URL,
        body={
            "result": [
                {"relationID": 700123, "projID": 102550, "partID": 102777, "relationType": 1},
                {"relationID": 700124, "projID": 102550, "partID": 102888, "relationType": 1},
            ],
            "modificationsHistory": None,
        },
    )
    async with IPSClient(config=token_config) as ips:
        rels = await ips.relation_create_collection(
            [
                CreateRelation(relation_type=1, proj_version_id=102550, part_version_id=102777),
                CreateRelation(relation_type=1, proj_version_id=102550, part_version_id=102888),
            ]
        )

    request = next(r for r in fake_ips.requests if r.path == COLLECTION_URL)
    body = request.body
    # Тело — голый JSON-массив CreateRelationDto.
    assert isinstance(body, list)
    assert body[0]["partVersionId"] == 102777
    assert body[1]["partVersionId"] == 102888
    # exclude_none: необязательный attributeValues отсутствует.
    assert "attributeValues" not in body[0]
    assert len(rels) == 2
    assert rels[1].relation_id == 700124


async def test_relation_create_collection_empty_result(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", COLLECTION_URL, body={"result": None, "modificationsHistory": None})
    async with IPSClient(config=token_config) as ips:
        rels = await ips.relation_create_collection([])

    request = next(r for r in fake_ips.requests if r.path == COLLECTION_URL)
    assert request.body == []
    assert rels == []


async def test_relation_delete_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.relation_delete(700123)
    # Без confirm запрос не отправляется.
    assert not [r for r in fake_ips.requests if r.method == "DELETE"]


async def test_relation_delete_builds_query(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("delete", DELETE_URL, body={"result": None})
    async with IPSClient(config=token_config) as ips:
        result = await ips.relation_delete(700123, confirm=True, delete_mode=2, log_history=False)

    request = next(r for r in fake_ips.requests if r.method == "DELETE" and r.path == DELETE_URL)
    assert request.query["relationId"] == "700123"
    assert request.query["deleteMode"] == "2"
    assert request.query["isNeedToLogModificationHistory"] == "false"
    # Тело DELETE — {} (на случай 415).
    assert request.body == {}
    assert result is None


async def test_relation_delete_omits_delete_mode(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("delete", DELETE_URL, body={"result": None})
    async with IPSClient(config=token_config) as ips:
        await ips.relation_delete(700123, confirm=True)

    request = next(r for r in fake_ips.requests if r.method == "DELETE" and r.path == DELETE_URL)
    # delete_mode=None -> параметр не передаётся.
    assert "deleteMode" not in request.query


async def test_relation_delete_attribute_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.relation_delete_attribute(700123, 205)
    assert not [r for r in fake_ips.requests if r.method == "DELETE"]


async def test_relation_delete_attribute_builds_path(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("delete", DELETE_ATTR_URL, body={"result": None})
    async with IPSClient(config=token_config) as ips:
        result = await ips.relation_delete_attribute(700123, 205, confirm=True, log_history=False)

    request = next(r for r in fake_ips.requests if r.path == DELETE_ATTR_URL)
    assert request.method == "DELETE"
    assert request.query["isNeedToLogModificationHistory"] == "false"
    assert request.body == {}
    assert result is None
