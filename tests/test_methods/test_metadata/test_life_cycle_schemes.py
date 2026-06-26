"""Тесты методов схем жизненного цикла раздела metadata."""

from uuid import UUID

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.common.enumerations import ObjectModifyMode

_SCHEME_GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"
_STEP_GUID = "11111111-2222-3333-4444-555555555555"

_SCHEME = {
    "id": 100,
    "guid": _SCHEME_GUID,
    "name": "Схема разработки",
    "note": None,
    "areaId": None,
    "options": 0,
    "default": True,
}

_LC_STEP = {
    "id": 10,
    "guid": _STEP_GUID,
    "schemeId": 100,
    "levelId": 0,
    "name": "В разработке",
    "note": None,
    "objectTypeId": 0,
    "accessType": "noCheck",
    "isDeleted": False,
    "objectModifyMode": "checkout",
    "isFirstStep": True,
    "options": None,
}


async def test_life_cycle_schemes_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/lifeCycleSchemes",
        body=[_SCHEME, _SCHEME],
    )
    async with IPSClient(config=token_config) as ips:
        schemes = await ips.life_cycle_schemes()

    assert len(schemes) == 2
    first = schemes[0]
    assert first.id == 100
    assert first.name == "Схема разработки"
    assert first.guid == UUID(_SCHEME_GUID)
    # JSON-ключ "default" → поле is_default
    assert first.is_default is True
    # options — целое число (битовая маска), не список
    assert first.options == 0
    # null-поля разворачиваются в None
    assert first.note is None
    assert first.area_id is None


async def test_life_cycle_scheme_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/lifeCycleSchemes/100",
        body={"entity": _SCHEME, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        scheme = await ips.life_cycle_scheme(100)

    assert scheme is not None
    assert scheme.id == 100
    assert scheme.is_default is True
    assert scheme.guid == UUID(_SCHEME_GUID)


async def test_life_cycle_scheme_returns_none_when_absent(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/lifeCycleSchemes/999",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        scheme = await ips.life_cycle_scheme(999)

    assert scheme is None


async def test_life_cycle_scheme_by_guid_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/lifeCycleSchemes/byGuid/{_SCHEME_GUID}",
        body={"entity": _SCHEME, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        scheme = await ips.life_cycle_scheme_by_guid(_SCHEME_GUID)

    assert scheme is not None
    assert scheme.guid == UUID(_SCHEME_GUID)
    assert scheme.name == "Схема разработки"


async def test_life_cycle_scheme_by_guid_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/lifeCycleSchemes/byGuid/{_SCHEME_GUID}",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        scheme = await ips.life_cycle_scheme_by_guid(_SCHEME_GUID)

    assert scheme is None


async def test_life_cycle_scheme_exists_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/lifeCycleSchemes/100/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        exists = await ips.life_cycle_scheme_exists(100)

    assert exists is True


async def test_life_cycle_scheme_exists_null_is_false(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/lifeCycleSchemes/999/exists", body=None)
    async with IPSClient(config=token_config) as ips:
        exists = await ips.life_cycle_scheme_exists(999)

    assert exists is False


async def test_life_cycle_scheme_exists_by_guid_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/lifeCycleSchemes/byGuid/{_SCHEME_GUID}/exists",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        exists = await ips.life_cycle_scheme_exists_by_guid(_SCHEME_GUID)

    assert exists is True


async def test_life_cycle_scheme_id_by_guid_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/lifeCycleSchemes/byGuid/{_SCHEME_GUID}/id",
        body=100,
    )
    async with IPSClient(config=token_config) as ips:
        scheme_id = await ips.life_cycle_scheme_id_by_guid(_SCHEME_GUID)

    assert scheme_id == 100
    assert isinstance(scheme_id, int)


async def test_life_cycle_scheme_name_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/lifeCycleSchemes/100/name",
        body="Схема разработки",
    )
    async with IPSClient(config=token_config) as ips:
        name = await ips.life_cycle_scheme_name(100)

    assert name == "Схема разработки"


async def test_life_cycle_scheme_name_null_is_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/lifeCycleSchemes/999/name", body=None)
    async with IPSClient(config=token_config) as ips:
        name = await ips.life_cycle_scheme_name(999)

    assert name == ""


async def test_life_cycle_scheme_name_by_guid_returns_str(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/lifeCycleSchemes/byGuid/{_SCHEME_GUID}/name",
        body="Схема разработки",
    )
    async with IPSClient(config=token_config) as ips:
        name = await ips.life_cycle_scheme_name_by_guid(_SCHEME_GUID)

    assert name == "Схема разработки"


async def test_life_cycle_scheme_guid_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/lifeCycleSchemes/100/guid",
        body=_SCHEME_GUID,
    )
    async with IPSClient(config=token_config) as ips:
        guid = await ips.life_cycle_scheme_guid(100)

    assert guid == _SCHEME_GUID


async def test_life_cycle_scheme_steps_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/lifeCycleSchemes/100/steps",
        body=[_LC_STEP],
    )
    async with IPSClient(config=token_config) as ips:
        steps = await ips.life_cycle_scheme_steps(100)

    assert len(steps) == 1
    step = steps[0]
    assert step.id == 10
    assert step.name == "В разработке"
    assert step.object_modify_mode == ObjectModifyMode.CHECKOUT
    assert step.is_first_step is True
    # options пришёл null — должен стать пустым списком
    assert step.options == []
    assert step.guid == UUID(_STEP_GUID)


async def test_life_cycle_scheme_steps_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/lifeCycleSchemes/999/steps", body=[])
    async with IPSClient(config=token_config) as ips:
        steps = await ips.life_cycle_scheme_steps(999)

    assert steps == []
