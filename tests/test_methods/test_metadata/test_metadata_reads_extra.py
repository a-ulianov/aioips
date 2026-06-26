"""Тесты дополнительных GET-методов раздела metadata (доступ по GUID).

Покрывают методы применяемости в GUID-пространстве (id/guid типов связи и
дочерних типов по GUID родителя), а также служебные ``displayable``/``globals``.
Проверяются: точный путь запроса, разбор голых массивов, разворот обёрток
``...NullableResultDto`` и семантика ``None`` (``isEntityPresent == false``).
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_TYPE_GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"
_RELATION_GUID = "11111111-2222-3333-4444-555555555555"


# --- applicability_relation_type_ids_by_guid() -------------------------------


async def test_applicability_relation_type_ids_by_guid_parses_bare_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/applicabilities/applicabilityRelationTypes/byGuid/{_TYPE_GUID}/ids",
        body=[501, 502],
    )
    async with IPSClient(config=token_config) as ips:
        ids = await ips.applicability_relation_type_ids_by_guid(_TYPE_GUID)

    assert ids == [501, 502]


async def test_applicability_relation_type_ids_by_guid_empty(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/applicabilities/applicabilityRelationTypes/byGuid/{_TYPE_GUID}/ids",
        body=[],
    )
    async with IPSClient(config=token_config) as ips:
        ids = await ips.applicability_relation_type_ids_by_guid(_TYPE_GUID)

    assert ids == []


# --- applicability_relation_type_guids_by_guid() -----------------------------


async def test_applicability_relation_type_guids_by_guid_parses_bare_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/applicabilities/applicabilityRelationTypes/byGuid/{_TYPE_GUID}/guids",
        body=[_RELATION_GUID],
    )
    async with IPSClient(config=token_config) as ips:
        guids = await ips.applicability_relation_type_guids_by_guid(_TYPE_GUID)

    assert guids == [_RELATION_GUID]


# --- applicability_child_object_type_ids_by_guids() --------------------------


async def test_applicability_child_object_type_ids_by_guids_unwraps_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/childObjectTypes/byGuids/"
        f"{_TYPE_GUID}/{_RELATION_GUID}/ids",
        body={"entity": [1755, 1756], "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        ids = await ips.applicability_child_object_type_ids_by_guids(_TYPE_GUID, _RELATION_GUID)

    assert ids == [1755, 1756]


async def test_applicability_child_object_type_ids_by_guids_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/childObjectTypes/byGuids/"
        f"{_TYPE_GUID}/{_RELATION_GUID}/ids",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        ids = await ips.applicability_child_object_type_ids_by_guids(_TYPE_GUID, _RELATION_GUID)

    assert ids is None


# --- applicability_child_object_type_guids_by_guids() ------------------------


async def test_applicability_child_object_type_guids_by_guids_unwraps_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/childObjectTypes/byGuids/"
        f"{_TYPE_GUID}/{_RELATION_GUID}/guids",
        body={"entity": [_TYPE_GUID], "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        guids = await ips.applicability_child_object_type_guids_by_guids(_TYPE_GUID, _RELATION_GUID)

    assert guids == [_TYPE_GUID]


async def test_applicability_child_object_type_guids_by_guids_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/childObjectTypes/byGuids/"
        f"{_TYPE_GUID}/{_RELATION_GUID}/guids",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        guids = await ips.applicability_child_object_type_guids_by_guids(_TYPE_GUID, _RELATION_GUID)

    assert guids is None


# --- displayable_by_guid() ---------------------------------------------------


async def test_displayable_by_guid_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/displayable/byGuid/{_TYPE_GUID}",
        body={"entity": {"text": "Деталь"}, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        view = await ips.displayable_by_guid(_TYPE_GUID)

    assert view == {"text": "Деталь"}


async def test_displayable_by_guid_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/displayable/byGuid/{_TYPE_GUID}",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        view = await ips.displayable_by_guid(_TYPE_GUID)

    assert view is None


# --- globals_by_guid() -------------------------------------------------------


async def test_globals_by_guid_returns_kind(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/globals/byGuid/{_TYPE_GUID}",
        body="imsObjectType",
    )
    async with IPSClient(config=token_config) as ips:
        kind = await ips.globals_by_guid(_TYPE_GUID)

    assert kind == "imsObjectType"


async def test_globals_by_guid_unknown(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/globals/byGuid/{_TYPE_GUID}",
        body="unknown",
    )
    async with IPSClient(config=token_config) as ips:
        kind = await ips.globals_by_guid(_TYPE_GUID)

    assert kind == "unknown"
