"""Тесты методов метаданных типов связей (relationTypes) раздела metadata."""

from uuid import UUID

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_REL_GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"
_TYPE_GUID = "11111111-2222-3333-4444-555555555555"

# Ключи строго по swagger ImsRelationTypeDto (camelCase).
_RELATION_TYPE = {
    "id": 501,
    "guid": _REL_GUID,
    "description": "Структурная связь",
    "typeName": "Входит в",
    "reverseName": "Состоит из",
    "checkOutFile": 1,
    "relationKind": 0,
    "areaId": None,
    "anyAttributes": True,
    "shortName": None,
    "note": None,
    "options": None,
}


async def test_relation_types_meta_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/relationTypes",
        body=[_RELATION_TYPE, _RELATION_TYPE],
    )
    async with IPSClient(config=token_config) as ips:
        items = await ips.relation_types_meta()

    assert len(items) == 2
    first = items[0]
    assert first.id == 501
    assert first.type_name == "Входит в"
    assert first.reverse_name == "Состоит из"
    assert first.relation_kind == 0
    assert first.check_out_file == 1
    assert first.guid == UUID(_REL_GUID)
    # options пришёл null — должен стать пустым списком
    assert first.options == []


async def test_relation_type_meta_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/relationTypes/501",
        body={"entity": _RELATION_TYPE, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        rel = await ips.relation_type_meta(501)

    assert rel is not None
    assert rel.id == 501
    assert rel.description == "Структурная связь"
    assert rel.any_attributes is True
    assert rel.guid == UUID(_REL_GUID)


async def test_relation_type_meta_returns_none_when_absent(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/relationTypes/999",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        rel = await ips.relation_type_meta(999)

    assert rel is None


async def test_relation_type_meta_by_guid_unwraps_entity(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/relationTypes/byGuid/{_REL_GUID}",
        body={"entity": _RELATION_TYPE, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        rel = await ips.relation_type_meta_by_guid(_REL_GUID)

    assert rel is not None
    assert rel.guid == UUID(_REL_GUID)
    assert rel.type_name == "Входит в"


async def test_relation_type_meta_by_guid_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/relationTypes/byGuid/{_REL_GUID}",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        rel = await ips.relation_type_meta_by_guid(_REL_GUID)

    assert rel is None


async def test_relation_type_meta_exists_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/relationTypes/501/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        exists = await ips.relation_type_meta_exists(501)

    assert exists is True


async def test_relation_type_meta_exists_by_guid_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/relationTypes/byGuid/{_REL_GUID}/exists",
        body=False,
    )
    async with IPSClient(config=token_config) as ips:
        exists = await ips.relation_type_meta_exists_by_guid(_REL_GUID)

    assert exists is False


async def test_relation_type_meta_id_by_guid_returns_int(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", f"/core/api/metadata/relationTypes/byGuid/{_REL_GUID}/id", body=501)
    async with IPSClient(config=token_config) as ips:
        rel_id = await ips.relation_type_meta_id_by_guid(_REL_GUID)

    assert rel_id == 501
    assert isinstance(rel_id, int)


async def test_relation_type_meta_name_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/relationTypes/501/name", body="Входит в")
    async with IPSClient(config=token_config) as ips:
        name = await ips.relation_type_meta_name(501)

    assert name == "Входит в"


async def test_relation_type_meta_name_handles_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/relationTypes/501/name", body=None)
    async with IPSClient(config=token_config) as ips:
        name = await ips.relation_type_meta_name(501)

    assert name == ""


async def test_relation_type_meta_name_by_guid_returns_str(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/relationTypes/byGuid/{_REL_GUID}/name",
        body="Входит в",
    )
    async with IPSClient(config=token_config) as ips:
        name = await ips.relation_type_meta_name_by_guid(_REL_GUID)

    assert name == "Входит в"


async def test_relation_type_meta_guid_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/relationTypes/501/guid", body=_REL_GUID)
    async with IPSClient(config=token_config) as ips:
        guid = await ips.relation_type_meta_guid(501)

    assert guid == _REL_GUID


async def test_default_relation_type_id_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/relationTypes/objectTypeDefault/1742/id",
        body=501,
    )
    async with IPSClient(config=token_config) as ips:
        rel_id = await ips.default_relation_type_id(1742)

    assert rel_id == 501
    assert isinstance(rel_id, int)


async def test_default_relation_type_guid_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/relationTypes/objectTypeDefault/1742/guid",
        body=_REL_GUID,
    )
    async with IPSClient(config=token_config) as ips:
        guid = await ips.default_relation_type_guid(1742)

    assert guid == _REL_GUID


async def test_default_relation_type_id_by_guid_returns_int(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/relationTypes/objectTypeDefault/byGuid/{_TYPE_GUID}/id",
        body=501,
    )
    async with IPSClient(config=token_config) as ips:
        rel_id = await ips.default_relation_type_id_by_guid(_TYPE_GUID)

    assert rel_id == 501


async def test_default_relation_type_guid_by_guid_returns_str(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/relationTypes/objectTypeDefault/byGuid/{_TYPE_GUID}/guid",
        body=_REL_GUID,
    )
    async with IPSClient(config=token_config) as ips:
        guid = await ips.default_relation_type_guid_by_guid(_TYPE_GUID)

    assert guid == _REL_GUID
