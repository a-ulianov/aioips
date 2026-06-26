"""Тесты READ-методов применяемости (applicabilities) раздела metadata."""

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


async def test_object_type_applicabilities_unwraps_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/objectTypeApplicabilities/1742",
        body={"entity": [_APPLICABILITY], "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        rules = await ips.object_type_applicabilities(1742)

    assert rules is not None
    assert len(rules) == 1
    rule = rules[0]
    assert rule.id == 7
    assert rule.in_object_type_id == 1742
    assert rule.child_object_type_id == 1755
    assert rule.relation_type_id == 501
    assert rule.is_content is True
    assert rule.relation_constraint_mode == "childConstrained"
    assert rule.public == InheritMode.PRIVATE
    # options пришёл null — должен стать пустым списком
    assert rule.options == []


async def test_object_type_applicabilities_returns_none_when_absent(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/objectTypeApplicabilities/999",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        rules = await ips.object_type_applicabilities(999)

    assert rules is None


async def test_object_type_parent_applicabilities_unwraps_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/objectTypeParentApplicabilities/1755",
        body={"entity": [_APPLICABILITY], "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        rules = await ips.object_type_parent_applicabilities(1755)

    assert rules is not None
    assert rules[0].in_object_type_id == 1742
    assert rules[0].child_object_type_id == 1755


async def test_object_type_parent_applicabilities_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/objectTypeParentApplicabilities/999",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        rules = await ips.object_type_parent_applicabilities(999)

    assert rules is None


async def test_child_object_type_ids_unwraps_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/metadata/applicabilities/childObjectTypes/byIds/1742/ids",
        body={"entity": [1755, 1756], "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        type_ids = await ips.child_object_type_ids(1742, [501])

    assert type_ids == [1755, 1756]
    # Тело запроса (список id типов связи) должно уйти на сервер как есть.
    sent = fake_ips.requests[-1]
    assert sent.method == "POST"
    assert sent.body == [501]


async def test_child_object_type_ids_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/metadata/applicabilities/childObjectTypes/byIds/999/ids",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        type_ids = await ips.child_object_type_ids(999, [501])

    assert type_ids is None


async def test_has_applicability_true(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/hasApplicability/1742",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.has_applicability(1742)

    assert result is True


async def test_has_applicability_false(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/applicabilities/hasApplicability/999",
        body=False,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.has_applicability(999)

    assert result is False
