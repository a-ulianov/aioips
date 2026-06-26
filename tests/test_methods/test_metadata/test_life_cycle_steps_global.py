"""Тесты глобальных аксессоров шагов жизненного цикла раздела metadata."""

from uuid import UUID

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.common.enumerations import ObjectModifyMode

_STEP_GUID = "11111111-2222-3333-4444-555555555555"
# GUID с символами, требующими кодирования в URL (для проверки quote).
_GUID_NEEDS_QUOTE = "a b/c"

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


async def test_life_cycle_steps_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    # Список — голый массив (без обёртки entity), как у attribute_types.
    fake_ips.add(
        "get",
        "/core/api/metadata/lifeCycleSteps",
        body=[_LC_STEP, _LC_STEP],
    )
    async with IPSClient(config=token_config) as ips:
        steps = await ips.life_cycle_steps()

    assert len(steps) == 2
    step = steps[0]
    assert step.id == 10
    assert step.name == "В разработке"
    assert step.object_modify_mode == ObjectModifyMode.CHECKOUT
    # options пришёл null — должен стать пустым списком
    assert step.options == []
    assert step.guid == UUID(_STEP_GUID)


async def test_life_cycle_steps_empty_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/lifeCycleSteps", body=[])
    async with IPSClient(config=token_config) as ips:
        steps = await ips.life_cycle_steps()

    assert steps == []


async def test_life_cycle_step_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/lifeCycleSteps/10",
        body={"entity": _LC_STEP, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        step = await ips.life_cycle_step(10)

    assert step is not None
    assert step.id == 10
    assert step.name == "В разработке"
    assert step.object_modify_mode == ObjectModifyMode.CHECKOUT
    assert step.is_first_step is True
    assert step.guid == UUID(_STEP_GUID)


async def test_life_cycle_step_returns_none_when_absent(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/lifeCycleSteps/999",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        step = await ips.life_cycle_step(999)

    assert step is None


async def test_life_cycle_step_by_guid_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/lifeCycleSteps/byGuid/{_STEP_GUID}",
        body={"entity": _LC_STEP, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        step = await ips.life_cycle_step_by_guid(_STEP_GUID)

    assert step is not None
    assert step.guid == UUID(_STEP_GUID)
    assert step.name == "В разработке"


async def test_life_cycle_step_by_guid_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/lifeCycleSteps/byGuid/{_STEP_GUID}",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        step = await ips.life_cycle_step_by_guid(_STEP_GUID)

    assert step is None


async def test_life_cycle_step_exists_true(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/lifeCycleSteps/10/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.life_cycle_step_exists(10)

    assert result is True


async def test_life_cycle_step_exists_false_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/lifeCycleSteps/999/exists", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.life_cycle_step_exists(999)

    assert result is False


async def test_life_cycle_step_exists_by_guid_true(token_config: IPSConfig, fake_ips: FakeIPS):
    # FakeIPS получает уже декодированный путь, поэтому мок по исходному GUID.
    fake_ips.add(
        "get",
        f"/core/api/metadata/lifeCycleSteps/byGuid/{_STEP_GUID}/exists",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.life_cycle_step_exists_by_guid(_STEP_GUID)

    assert result is True


async def test_life_cycle_step_exists_by_guid_encodes_guid(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    # Декодированный путь содержит пробел и слэш — значит quote(safe="") отработал.
    fake_ips.add(
        "get",
        f"/core/api/metadata/lifeCycleSteps/byGuid/{_GUID_NEEDS_QUOTE}/exists",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.life_cycle_step_exists_by_guid(_GUID_NEEDS_QUOTE)

    assert result is True


async def test_life_cycle_step_id_by_guid_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/lifeCycleSteps/byGuid/{_STEP_GUID}/id",
        body=10,
    )
    async with IPSClient(config=token_config) as ips:
        step_id = await ips.life_cycle_step_id_by_guid(_STEP_GUID)

    assert step_id == 10
    assert isinstance(step_id, int)


async def test_life_cycle_step_name_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/lifeCycleSteps/10/name", body="В разработке")
    async with IPSClient(config=token_config) as ips:
        name = await ips.life_cycle_step_name(10)

    assert name == "В разработке"


async def test_life_cycle_step_name_empty_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/lifeCycleSteps/999/name", body=None)
    async with IPSClient(config=token_config) as ips:
        name = await ips.life_cycle_step_name(999)

    assert name == ""


async def test_life_cycle_step_name_by_guid_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/lifeCycleSteps/byGuid/{_STEP_GUID}/name",
        body="В разработке",
    )
    async with IPSClient(config=token_config) as ips:
        name = await ips.life_cycle_step_name_by_guid(_STEP_GUID)

    assert name == "В разработке"


async def test_life_cycle_step_guid_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/lifeCycleSteps/10/guid", body=_STEP_GUID)
    async with IPSClient(config=token_config) as ips:
        guid = await ips.life_cycle_step_guid(10)

    assert guid == _STEP_GUID
