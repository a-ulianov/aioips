"""Тесты методов чтения базовой версии и состава объекта."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_BASE_OBJECT = {
    "objectID": 102550,
    "id": 5005,
    "versionID": 3,
    "objectType": 1127,
    "caption": "Деталь А",
    "isBaseVersion": True,
}
_PART_A = {"objectID": 200001, "id": 6001, "objectType": 1127, "caption": "Болт"}
_PART_B = {"objectID": 200002, "id": 6002, "objectType": 1127, "caption": "Гайка"}


async def test_object_base_version_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/objects/102550/baseVersion",
        body={"entity": _BASE_OBJECT, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        obj = await ips.object_base_version(102550)

    assert obj is not None
    assert obj.object_id == 102550
    assert obj.is_base_version is True
    assert obj.version_id == 3


async def test_object_base_version_returns_none_when_absent(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/objects/999/baseVersion",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        obj = await ips.object_base_version(999)

    assert obj is None


async def test_object_composition_extracts_object_field(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/102550/compositionWithParams",
        body=[
            {"object": _PART_A, "relation": {"relationID": 11}},
            {"object": _PART_B, "relation": {"relationID": 12}},
        ],
    )
    async with IPSClient(config=token_config) as ips:
        parts = await ips.object_composition_with_params(
            102550, relation_type_id=4, part_type_ids=[1127]
        )

    assert len(parts) == 2
    assert [p.object_id for p in parts] == [200001, 200002]
    assert parts[0].caption == "Болт"


async def test_object_composition_none_part_types_sent_as_empty_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/objects/102550/compositionWithParams", body=[])
    async with IPSClient(config=token_config) as ips:
        await ips.object_composition_with_params(102550, relation_type_id=4)

    request = next(
        r for r in fake_ips.requests if r.path == "/core/api/objects/102550/compositionWithParams"
    )
    assert request.body == {"relationTypeId": 4, "partTypeIds": []}


async def test_object_composition_skips_null_objects(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/102550/compositionWithParams",
        body=[{"object": None, "relation": {"relationID": 11}}, {"object": _PART_A}],
    )
    async with IPSClient(config=token_config) as ips:
        parts = await ips.object_composition_with_params(102550, part_type_ids=[1127])

    assert len(parts) == 1
    assert parts[0].object_id == 200001
