"""Тесты дополнительных методов чтения раздела прав доступа (безопасности).

Покрывают read-методы прав на систему, разделы метаданных (предметные области,
языки, атрибуты/группы, типы связей, уровни/схемы ЖЦ) и контекстно-зависимые
права на шаг ЖЦ типа объекта и атрибут на шаге. Каждый метод проверяется на
точность пути запроса и корректный разбор :class:`Security`.
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

# Полный снимок прав; ключи — точно как в SecurityDto (camelCase).
_SECURITY: dict[str, object] = {
    "securityName": "System",
    "categoryType": 1,
    "categoryId": 0,
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
    "durations": [],
    "conditions": [],
    "isConditionsEnabled": False,
    "relatedSecurities": [],
}


def _assert_security(sec) -> None:
    """Проверяет базовый разбор снимка прав и вложенных DTO."""
    assert sec.targets[0].target_id == 500
    assert sec.actions[0].action_id == "read"
    assert sec.permissions[0].access_type == "grant"


async def test_system_security(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/security/system", body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.system_security()

    _assert_security(sec)
    assert fake_ips.requests[-1].path == "/core/api/security/system"


async def test_subject_areas_security(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/security/subjectAreas", body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.subject_areas_security()

    _assert_security(sec)
    assert fake_ips.requests[-1].path == "/core/api/security/subjectAreas"


async def test_languages_security(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/security/languages", body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.languages_security()

    _assert_security(sec)
    assert fake_ips.requests[-1].path == "/core/api/security/languages"


async def test_attributes_collection_security(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/security/attributes", body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.attributes_collection_security()

    _assert_security(sec)
    assert fake_ips.requests[-1].path == "/core/api/security/attributes"


async def test_attribute_groups_security(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/security/attributeGroups", body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.attribute_groups_security()

    _assert_security(sec)
    assert fake_ips.requests[-1].path == "/core/api/security/attributeGroups"


async def test_attribute_group_security(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/security/attributeGroups/42", body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.attribute_group_security(42)

    _assert_security(sec)
    assert fake_ips.requests[-1].path == "/core/api/security/attributeGroups/42"


async def test_relation_types_security(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/security/relationTypes", body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.relation_types_security()

    _assert_security(sec)
    assert fake_ips.requests[-1].path == "/core/api/security/relationTypes"


async def test_relation_type_security(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/security/relationTypes/7", body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.relation_type_security(7)

    _assert_security(sec)
    assert fake_ips.requests[-1].path == "/core/api/security/relationTypes/7"


async def test_lifecycle_levels_security(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/security/lifecycleLevels", body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.lifecycle_levels_security()

    _assert_security(sec)
    assert fake_ips.requests[-1].path == "/core/api/security/lifecycleLevels"


async def test_lifecycle_level_security(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/security/lifecycleLevels/3", body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.lifecycle_level_security(3)

    _assert_security(sec)
    assert fake_ips.requests[-1].path == "/core/api/security/lifecycleLevels/3"


async def test_lifecycle_schemes_security(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/security/lifecycleSchemes", body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.lifecycle_schemes_security()

    _assert_security(sec)
    assert fake_ips.requests[-1].path == "/core/api/security/lifecycleSchemes"


async def test_lifecycle_scheme_security(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/security/lifecycleSchemes/15", body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.lifecycle_scheme_security(15)

    _assert_security(sec)
    assert fake_ips.requests[-1].path == "/core/api/security/lifecycleSchemes/15"


async def test_object_type_lifecycle_step_security(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/objectTypes/1031/lifecycleSchemeSteps/5"
    fake_ips.add("get", path, body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.object_type_lifecycle_step_security(1031, 5)

    _assert_security(sec)
    assert fake_ips.requests[-1].path == path


async def test_object_type_lifecycle_step_attribute_security(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = "/core/api/security/objectTypes/1031/lifecycleSchemeSteps/5/attributes/1029"
    fake_ips.add("get", path, body=_SECURITY)
    async with IPSClient(config=token_config) as ips:
        sec = await ips.object_type_lifecycle_step_attribute_security(1031, 5, 1029)

    _assert_security(sec)
    assert fake_ips.requests[-1].path == path
