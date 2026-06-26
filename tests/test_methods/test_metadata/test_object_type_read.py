"""Тесты методов чтения типов объектов и шагов ЖЦ раздела metadata."""

from uuid import UUID

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.common.enumerations import ObjectModifyMode, ObjectVersionMode

_TYPE_GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"
_STEP_GUID = "11111111-2222-3333-4444-555555555555"

_OBJECT_TYPE = {
    "id": 1742,
    "guid": _TYPE_GUID,
    "objectTypeName": "Document",
    "objectName": "Документ",
    "versionsMode": "multiVersion",
    "options": None,
}

_QUICK_OBJECT = {
    "caption": "Чертёж 01",
    "objectTypeID": 1742,
    "objectID": 4,
    "versionGuid": _STEP_GUID,
    "id": 5,
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


async def test_object_type_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/objectTypes/1742",
        body={"entity": _OBJECT_TYPE, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        object_type = await ips.object_type(1742)

    assert object_type is not None
    assert object_type.id == 1742
    assert object_type.object_name == "Документ"
    assert object_type.versions_mode == ObjectVersionMode.MULTI_VERSION
    # options пришёл null — должен стать пустым списком
    assert object_type.options == []
    assert object_type.guid == UUID(_TYPE_GUID)


async def test_object_type_returns_none_when_absent(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/objectTypes/999",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        object_type = await ips.object_type(999)

    assert object_type is None


async def test_object_type_by_guid_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/objectTypes/byGuid/{_TYPE_GUID}",
        body={"entity": _OBJECT_TYPE, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        object_type = await ips.object_type_by_guid(_TYPE_GUID)

    assert object_type is not None
    assert object_type.guid == UUID(_TYPE_GUID)
    assert object_type.object_type_name == "Document"


async def test_object_type_by_guid_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/objectTypes/byGuid/{_TYPE_GUID}",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        object_type = await ips.object_type_by_guid(_TYPE_GUID)

    assert object_type is None


async def test_object_type_id_by_name_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    # Имя кодируется в URL, но aiohttp на сервере отдаёт уже декодированный path,
    # поэтому мок регистрируем по исходному (декодированному) пути.
    fake_ips.add(
        "get",
        "/core/api/metadata/objectTypes/byName/Документ/id",
        body=1742,
    )
    async with IPSClient(config=token_config) as ips:
        type_id = await ips.object_type_id_by_name("Документ")

    assert type_id == 1742
    assert isinstance(type_id, int)


async def test_objects_by_object_type_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/objectTypes/1742/objects",
        body=[_QUICK_OBJECT, _QUICK_OBJECT],
    )
    async with IPSClient(config=token_config) as ips:
        items = await ips.objects_by_object_type(1742)

    assert len(items) == 2
    first = items[0]
    # object_id (=objectID) — идентификатор объекта, id — идентификатор версии
    assert first.object_id == 4
    assert first.id == 5
    assert first.object_type_id == 1742
    assert first.caption == "Чертёж 01"
    assert first.version_guid == UUID(_STEP_GUID)


async def test_object_type_life_cycle_steps_unwraps_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/objectTypes/1742/lifeCycleSteps",
        body={"entity": [_LC_STEP], "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        steps = await ips.object_type_life_cycle_steps(1742)

    assert steps is not None
    assert len(steps) == 1
    step = steps[0]
    assert step.id == 10
    assert step.name == "В разработке"
    assert step.object_modify_mode == ObjectModifyMode.CHECKOUT
    assert step.access_type == "noCheck"
    assert step.is_first_step is True
    # options пришёл null — должен стать пустым списком
    assert step.options == []
    assert step.guid == UUID(_STEP_GUID)


async def test_object_type_life_cycle_steps_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/objectTypes/999/lifeCycleSteps",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        steps = await ips.object_type_life_cycle_steps(999)

    assert steps is None
