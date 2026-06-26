"""Тесты методов-аксессоров применяемости (applicabilities) раздела metadata.

Покрывают новые методы матрицы применяемости: полный список, адресную тройку,
доступ по GUID, булевы предикаты, развороты потомков (типы/id/guid) и плоские
справочники типов связи и типов-участников. Проверяется разворот обёрток
``...NullableResultDto`` (список и одиночный), прямой разбор голых массивов и
семантика ``None`` при отсутствии сущности.
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.common.enumerations import InheritMode

# Пример записи применяемости (ImsApplicabilityDto): объект типа 1755 может входить
# по связи 501 в состав объекта типа 1742.
_APPLICABILITY = {
    "id": 7,
    "relationTypeId": 501,
    "inObjectTypeId": 1742,
    "childObjectTypeId": 1755,
    "cloneChildRelations": False,
    "checkoutFiles": False,
    "maximumLinks": 2147483647,
    "relationConstraintMode": "childConstrained",
    "applicabilityMode": "enabled",
    "isContent": True,
    "options": None,
    "public": "private",
}

_TYPE_GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"
_RELATION_GUID = "11111111-2222-3333-4444-555555555555"

_OBJECT_TYPE = {
    "id": 1755,
    "guid": _TYPE_GUID,
    "objectTypeName": "Part",
    "objectName": "Деталь",
    "versionsMode": "multiVersion",
    "options": None,
}


# --- applicabilities() -------------------------------------------------------


async def test_applicabilities_parses_bare_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/applicabilities", body=[_APPLICABILITY])
    async with IPSClient(config=token_config) as ips:
        rules = await ips.applicabilities()

    assert len(rules) == 1
    assert rules[0].in_object_type_id == 1742
    assert rules[0].child_object_type_id == 1755
    assert rules[0].public == InheritMode.PRIVATE


async def test_applicabilities_empty_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/applicabilities", body=[])
    async with IPSClient(config=token_config) as ips:
        rules = await ips.applicabilities()

    assert rules == []


# --- applicability() ---------------------------------------------------------


async def test_applicability_unwraps_single(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/1742/1755/501",
        body={"entity": _APPLICABILITY, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        rule = await ips.applicability(1742, 1755, 501)

    assert rule is not None
    assert rule.id == 7
    assert rule.maximum_links == 2147483647


async def test_applicability_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/1/2/3",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        rule = await ips.applicability(1, 2, 3)

    assert rule is None


# --- object_type_applicabilities_by_guid() -----------------------------------


async def test_object_type_applicabilities_by_guid_unwraps_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/applicabilities/objectTypeApplicabilities/byGuid/{_TYPE_GUID}",
        body={"entity": [_APPLICABILITY], "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        rules = await ips.object_type_applicabilities_by_guid(_TYPE_GUID)

    assert rules is not None
    assert rules[0].child_object_type_id == 1755


async def test_object_type_applicabilities_by_guid_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/applicabilities/objectTypeApplicabilities/byGuid/{_TYPE_GUID}",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        rules = await ips.object_type_applicabilities_by_guid(_TYPE_GUID)

    assert rules is None


# --- has_applicability_full() ------------------------------------------------


async def test_has_applicability_full_true(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/hasApplicability/1742/1755/501",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        assert await ips.has_applicability_full(1742, 1755, 501) is True


async def test_has_applicability_full_false(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/hasApplicability/1/2/3",
        body=False,
    )
    async with IPSClient(config=token_config) as ips:
        assert await ips.has_applicability_full(1, 2, 3) is False


# --- has_applicability_by_guid() ---------------------------------------------


async def test_has_applicability_by_guid_true(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/applicabilities/hasApplicability/byGuid/{_TYPE_GUID}",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        assert await ips.has_applicability_by_guid(_TYPE_GUID) is True


# --- can_enters_in() ---------------------------------------------------------


async def test_can_enters_in_true(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/canEntersIn/1755",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        assert await ips.can_enters_in(1755) is True


async def test_can_enters_in_false(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/canEntersIn/999",
        body=False,
    )
    async with IPSClient(config=token_config) as ips:
        assert await ips.can_enters_in(999) is False


# --- applicability_child_object_types() --------------------------------------


async def test_applicability_child_object_types_unwraps_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/childObjectTypes/byIds/1742/501",
        body={"entity": [_OBJECT_TYPE], "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        types = await ips.applicability_child_object_types(1742, 501)

    assert types is not None
    assert types[0].id == 1755
    assert types[0].object_name == "Деталь"


async def test_applicability_child_object_types_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/childObjectTypes/byIds/999/501",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        types = await ips.applicability_child_object_types(999, 501)

    assert types is None


# --- applicability_child_object_type_ids() -----------------------------------


async def test_applicability_child_object_type_ids_unwraps_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/childObjectTypes/byIds/1742/501/ids",
        body={"entity": [1755, 1756], "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        ids = await ips.applicability_child_object_type_ids(1742, 501)

    assert ids == [1755, 1756]


async def test_applicability_child_object_type_ids_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/childObjectTypes/byIds/999/501/ids",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        ids = await ips.applicability_child_object_type_ids(999, 501)

    assert ids is None


# --- applicability_child_object_type_guids() ---------------------------------


async def test_applicability_child_object_type_guids_unwraps_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/childObjectTypes/byIds/1742/501/guids",
        body={"entity": [_TYPE_GUID], "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        guids = await ips.applicability_child_object_type_guids(1742, 501)

    assert guids == [_TYPE_GUID]


async def test_applicability_child_object_type_guids_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/childObjectTypes/byIds/999/501/guids",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        guids = await ips.applicability_child_object_type_guids(999, 501)

    assert guids is None


# --- applicability_child_object_types_by_guids() -----------------------------


async def test_applicability_child_object_types_by_guids_unwraps_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/applicabilities/childObjectTypes/byGuids/{_TYPE_GUID}/{_RELATION_GUID}",
        body={"entity": [_OBJECT_TYPE], "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        types = await ips.applicability_child_object_types_by_guids(_TYPE_GUID, _RELATION_GUID)

    assert types is not None
    assert types[0].id == 1755


async def test_applicability_child_object_types_by_guids_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/applicabilities/childObjectTypes/byGuids/{_TYPE_GUID}/{_RELATION_GUID}",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        types = await ips.applicability_child_object_types_by_guids(_TYPE_GUID, _RELATION_GUID)

    assert types is None


# --- applicability_relation_type_ids() / guids() -----------------------------


async def test_applicability_relation_type_ids_parses_bare_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/applicabilityRelationTypes/1742/ids",
        body=[501, 502],
    )
    async with IPSClient(config=token_config) as ips:
        ids = await ips.applicability_relation_type_ids(1742)

    assert ids == [501, 502]


async def test_applicability_relation_type_guids_parses_bare_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/applicabilityRelationTypes/1742/guids",
        body=[_RELATION_GUID],
    )
    async with IPSClient(config=token_config) as ips:
        guids = await ips.applicability_relation_type_guids(1742)

    assert guids == [_RELATION_GUID]


# --- object_types_with_(enter_in_)applicabilities_ids() ----------------------


async def test_object_types_with_applicabilities_ids_parses_bare_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/objectTypesWithApplicabilities/ids",
        body=[1742, 1743],
    )
    async with IPSClient(config=token_config) as ips:
        ids = await ips.object_types_with_applicabilities_ids()

    assert ids == [1742, 1743]


async def test_object_types_with_enter_in_applicabilities_ids_parses_bare_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/objectTypesWithEnterInApplicabilities/ids",
        body=[1755, 1756],
    )
    async with IPSClient(config=token_config) as ips:
        ids = await ips.object_types_with_enter_in_applicabilities_ids()

    assert ids == [1755, 1756]
