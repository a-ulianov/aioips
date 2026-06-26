"""Тесты методов уровней жизненного цикла раздела metadata.

Предусловие: миксины уровней ЖЦ должны быть подключены к ``MetadataAPI`` в
``methods/metadata/__init__.py`` (см. отчёт по задаче) — тесты обращаются к
методам через публичный фасад :class:`IPSClient`.
"""

from uuid import UUID

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_LEVEL_GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"
# GUID с символами, требующими кодирования в URL (для проверки quote).
_GUID_NEEDS_QUOTE = "a b/c"

_LEVEL = {
    "id": 3,
    "guid": _LEVEL_GUID,
    "name": "Утверждено",
    "areaId": None,
    "litera": None,
    "storageId": 0,
    "default": True,
}


async def test_life_cycle_levels_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/lifeCycleLevels", body=[_LEVEL, _LEVEL])
    async with IPSClient(config=token_config) as ips:
        levels = await ips.life_cycle_levels()

    assert len(levels) == 2
    first = levels[0]
    assert first.id == 3
    assert first.name == "Утверждено"
    assert first.guid == UUID(_LEVEL_GUID)
    # areaId/litera пришли null — должны стать None
    assert first.area_id is None
    assert first.litera is None
    assert first.storage_id == 0
    # JSON-ключ "default" маппится на is_default
    assert first.is_default is True


async def test_life_cycle_level_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/lifeCycleLevels/3",
        body={"entity": _LEVEL, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        level = await ips.life_cycle_level(3)

    assert level is not None
    assert level.id == 3
    assert level.name == "Утверждено"
    assert level.is_default is True
    assert level.guid == UUID(_LEVEL_GUID)


async def test_life_cycle_level_returns_none_when_absent(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/lifeCycleLevels/999",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        level = await ips.life_cycle_level(999)

    assert level is None


async def test_life_cycle_level_by_guid_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/lifeCycleLevels/byGuid/{_LEVEL_GUID}",
        body={"entity": _LEVEL, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        level = await ips.life_cycle_level_by_guid(_LEVEL_GUID)

    assert level is not None
    assert level.guid == UUID(_LEVEL_GUID)
    assert level.id == 3


async def test_life_cycle_level_by_guid_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/lifeCycleLevels/byGuid/{_LEVEL_GUID}",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        level = await ips.life_cycle_level_by_guid(_LEVEL_GUID)

    assert level is None


async def test_life_cycle_level_exists_true(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/lifeCycleLevels/3/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.life_cycle_level_exists(3)

    assert result is True


async def test_life_cycle_level_exists_false_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/lifeCycleLevels/999/exists", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.life_cycle_level_exists(999)

    assert result is False


async def test_life_cycle_level_exists_by_guid_true(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/lifeCycleLevels/byGuid/{_LEVEL_GUID}/exists",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.life_cycle_level_exists_by_guid(_LEVEL_GUID)

    assert result is True


async def test_life_cycle_level_exists_by_guid_encodes_guid(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    # Декодированный путь содержит пробел и слэш — значит quote(safe="") отработал.
    fake_ips.add(
        "get",
        f"/core/api/metadata/lifeCycleLevels/byGuid/{_GUID_NEEDS_QUOTE}/exists",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.life_cycle_level_exists_by_guid(_GUID_NEEDS_QUOTE)

    assert result is True


async def test_life_cycle_level_id_by_guid_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/lifeCycleLevels/byGuid/{_LEVEL_GUID}/id",
        body=3,
    )
    async with IPSClient(config=token_config) as ips:
        level_id = await ips.life_cycle_level_id_by_guid(_LEVEL_GUID)

    assert level_id == 3
    assert isinstance(level_id, int)


async def test_life_cycle_level_name_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/lifeCycleLevels/3/name", body="Утверждено")
    async with IPSClient(config=token_config) as ips:
        name = await ips.life_cycle_level_name(3)

    assert name == "Утверждено"


async def test_life_cycle_level_name_empty_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/lifeCycleLevels/999/name", body=None)
    async with IPSClient(config=token_config) as ips:
        name = await ips.life_cycle_level_name(999)

    assert name == ""


async def test_life_cycle_level_name_by_guid_returns_str(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/lifeCycleLevels/byGuid/{_LEVEL_GUID}/name",
        body="Утверждено",
    )
    async with IPSClient(config=token_config) as ips:
        name = await ips.life_cycle_level_name_by_guid(_LEVEL_GUID)

    assert name == "Утверждено"


async def test_life_cycle_level_guid_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/lifeCycleLevels/3/guid", body=_LEVEL_GUID)
    async with IPSClient(config=token_config) as ips:
        guid = await ips.life_cycle_level_guid(3)

    assert guid == _LEVEL_GUID


async def test_life_cycle_level_guid_empty_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/lifeCycleLevels/3/guid", body=None)
    async with IPSClient(config=token_config) as ips:
        guid = await ips.life_cycle_level_guid(3)

    assert guid == ""
