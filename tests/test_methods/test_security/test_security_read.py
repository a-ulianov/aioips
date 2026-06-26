"""Тесты методов чтения раздела прав доступа (безопасности)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

# Полный снимок прав с вложенными DTO; ключи — точно как в SecurityDto (camelCase).
_SECURITY = {
    "securityName": "ObjectType_1031",
    "categoryType": 2,
    "categoryId": 1031,
    "targets": [
        {
            "targetId": 500,
            "targetTypeId": 12,
            "targetName": "Конструкторы",
            "isFullDefaultPermissions": False,
        }
    ],
    "actions": [
        {
            "actionId": "read",
            "actionName": "Чтение",
            "actionCategoryId": "read",
            "actionCategoryName": "Читать",
            "isAllowByDefault": True,
            "relatedActionIds": [1, 2],
        }
    ],
    "permissions": [
        {
            "actionId": "edit",
            "targetId": 500,
            "accessType": "grant",
            "isDefaultPermission": False,
        }
    ],
    "durations": [
        {
            "targetId": 500,
            "startDateTime": "2026-01-01T00:00:00Z",
            "endDateTime": "2026-12-31T23:59:59Z",
        }
    ],
    "conditions": [{"targetId": 500, "conditionId": 7}],
    "isConditionsEnabled": True,
    "relatedSecurities": [],
}


def _assert_full_security(sec) -> None:
    """Проверяет разбор полного снимка прав и вложенных DTO."""
    assert sec.security_name == "ObjectType_1031"
    assert sec.category_type == 2
    assert sec.category_id == 1031
    assert sec.is_conditions_enabled is True

    assert sec.targets[0].target_id == 500
    assert sec.targets[0].target_type_id == 12
    assert sec.targets[0].target_name == "Конструкторы"
    assert sec.targets[0].is_full_default_permissions is False

    assert sec.actions[0].action_id == "read"
    assert sec.actions[0].action_category_id == "read"
    assert sec.actions[0].is_allow_by_default is True
    assert sec.actions[0].related_action_ids == [1, 2]

    assert sec.permissions[0].action_id == "edit"
    assert sec.permissions[0].target_id == 500
    assert sec.permissions[0].access_type == "grant"

    assert sec.durations[0].target_id == 500
    assert sec.durations[0].start_date_time is not None

    assert sec.conditions[0].target_id == 500
    assert sec.conditions[0].condition_id == 7


async def test_object_security(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/security/objects/204931", body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.object_security(204931)

    _assert_full_security(sec)
    assert fake_ips.requests[-1].path == "/core/api/security/objects/204931"


async def test_object_type_security(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/security/objectTypes/1031", body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.object_type_security(1031)

    assert sec.category_id == 1031
    assert sec.permissions[0].access_type == "grant"
    assert fake_ips.requests[-1].path == "/core/api/security/objectTypes/1031"


async def test_object_types_security(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/security/objectTypes", body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.object_types_security()

    _assert_full_security(sec)
    assert fake_ips.requests[-1].path == "/core/api/security/objectTypes"


async def test_attribute_security(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/security/attributes/1029", body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.attribute_security(1029)

    assert sec.actions[0].action_id == "read"
    assert fake_ips.requests[-1].path == "/core/api/security/attributes/1029"


async def test_actions_on_objects_security(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/security/actionOnObjects", body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.actions_on_objects_security()

    _assert_full_security(sec)
    assert fake_ips.requests[-1].path == "/core/api/security/actionOnObjects"


async def test_security_coerces_null_lists(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {
        "securityName": None,
        "categoryType": 0,
        "categoryId": 0,
        "targets": None,
        "actions": None,
        "permissions": None,
        "durations": None,
        "conditions": None,
        "isConditionsEnabled": False,
        "relatedSecurities": None,
    }
    fake_ips.add("get", "/core/api/security/objectTypes", body=body)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.object_types_security()

    assert sec.targets == []
    assert sec.actions == []
    assert sec.permissions == []
    assert sec.durations == []
    assert sec.conditions == []
    assert sec.related_securities == []


async def test_security_related_recursion(token_config: IPSConfig, fake_ips: FakeIPS):
    nested = {**_SECURITY, "relatedSecurities": []}
    body = {**_SECURITY, "relatedSecurities": [nested]}
    fake_ips.add("get", "/core/api/security/objects/1", body=body)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.object_security(1)

    assert len(sec.related_securities) == 1
    inner = sec.related_securities[0]
    assert inner.category_id == 1031
    assert inner.permissions[0].action_id == "edit"
