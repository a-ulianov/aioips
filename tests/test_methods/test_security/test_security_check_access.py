"""Тесты методов проверки доступа (``checkAccess``) раздела безопасности.

Проверяют для каждого метода: корректный путь POST, сериализацию тела
(``CheckAccessDto`` с алиасами ``actionType`` / ``defaultAccess`` / ``throwACException``)
и интерпретацию голого ``boolean``-ответа в ``bool``.
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.security import SecurityCheckAccess


async def test_check_system_security_access_true(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/system/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_system_security_access(
            SecurityCheckAccess(action_type="setAccess")
        )

    assert result is True
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/core/api/security/system/checkAccess"
    assert req.body == {"actionType": "setAccess", "throwACException": False}


async def test_check_system_security_access_false(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/system/checkAccess", body=False)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_system_security_access(
            SecurityCheckAccess(action_type="setAccess")
        )

    assert result is False


async def test_check_access_serializes_all_fields_with_aliases(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    """Все поля DTO уходят в тело под camelCase-алиасами (включая throwACException)."""
    fake_ips.add("post", "/core/api/security/system/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        await ips.check_system_security_access(
            SecurityCheckAccess(action_type="read", default_access=True, throw_ac_exception=True)
        )

    assert fake_ips.requests[-1].body == {
        "actionType": "read",
        "defaultAccess": True,
        "throwACException": True,
    }


async def test_check_access_excludes_none_default_access(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    """``default_access=None`` не сериализуется (exclude_none); остаётся дефолт цели."""
    fake_ips.add("post", "/core/api/security/system/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        await ips.check_system_security_access(SecurityCheckAccess(action_type="read"))

    body = fake_ips.requests[-1].body
    assert "defaultAccess" not in body  # type: ignore[operator]
    assert body == {"actionType": "read", "throwACException": False}


async def test_check_access_none_body_is_false(token_config: IPSConfig, fake_ips: FakeIPS):
    """Пустой/``null`` ответ трактуется как отсутствие прав (fail-closed)."""
    fake_ips.add("post", "/core/api/security/system/checkAccess", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_system_security_access(SecurityCheckAccess(action_type="read"))

    assert result is False


async def test_check_actions_on_objects_security_access(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/actionOnObjects/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_actions_on_objects_security_access(
            SecurityCheckAccess(action_type="read")
        )

    assert result is True
    assert fake_ips.requests[-1].path == "/core/api/security/actionOnObjects/checkAccess"


async def test_check_attribute_groups_security_access(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/attributeGroups/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_attribute_groups_security_access(
            SecurityCheckAccess(action_type="read")
        )

    assert result is True
    assert fake_ips.requests[-1].path == "/core/api/security/attributeGroups/checkAccess"


async def test_check_attribute_group_security_access(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/attributeGroups/42/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_attribute_group_security_access(
            42, SecurityCheckAccess(action_type="read")
        )

    assert result is True
    assert fake_ips.requests[-1].path == "/core/api/security/attributeGroups/42/checkAccess"
    assert fake_ips.requests[-1].body == {"actionType": "read", "throwACException": False}


async def test_check_attributes_security_access(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/attributes/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_attributes_security_access(SecurityCheckAccess(action_type="read"))

    assert result is True
    assert fake_ips.requests[-1].path == "/core/api/security/attributes/checkAccess"


async def test_check_attribute_security_access(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/attributes/1029/checkAccess", body=False)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_attribute_security_access(
            1029, SecurityCheckAccess(action_type="edit")
        )

    assert result is False
    assert fake_ips.requests[-1].path == "/core/api/security/attributes/1029/checkAccess"
    assert fake_ips.requests[-1].body == {"actionType": "edit", "throwACException": False}


async def test_check_languages_security_access(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/languages/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_languages_security_access(SecurityCheckAccess(action_type="read"))

    assert result is True
    assert fake_ips.requests[-1].path == "/core/api/security/languages/checkAccess"


async def test_check_lifecycle_levels_security_access(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/lifecycleLevels/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_lifecycle_levels_security_access(
            SecurityCheckAccess(action_type="read")
        )

    assert result is True
    assert fake_ips.requests[-1].path == "/core/api/security/lifecycleLevels/checkAccess"


async def test_check_lifecycle_level_security_access(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/lifecycleLevels/3/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_lifecycle_level_security_access(
            3, SecurityCheckAccess(action_type="read")
        )

    assert result is True
    assert fake_ips.requests[-1].path == "/core/api/security/lifecycleLevels/3/checkAccess"


async def test_check_lifecycle_schemes_security_access(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/lifecycleSchemes/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_lifecycle_schemes_security_access(
            SecurityCheckAccess(action_type="read")
        )

    assert result is True
    assert fake_ips.requests[-1].path == "/core/api/security/lifecycleSchemes/checkAccess"


async def test_check_lifecycle_scheme_security_access(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/lifecycleSchemes/7/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_lifecycle_scheme_security_access(
            7, SecurityCheckAccess(action_type="read")
        )

    assert result is True
    assert fake_ips.requests[-1].path == "/core/api/security/lifecycleSchemes/7/checkAccess"


async def test_check_object_types_security_access(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/objectTypes/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_object_types_security_access(
            SecurityCheckAccess(action_type="create")
        )

    assert result is True
    assert fake_ips.requests[-1].path == "/core/api/security/objectTypes/checkAccess"


async def test_check_object_type_security_access(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/objectTypes/1031/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_object_type_security_access(
            1031, SecurityCheckAccess(action_type="create")
        )

    assert result is True
    assert fake_ips.requests[-1].path == "/core/api/security/objectTypes/1031/checkAccess"
    assert fake_ips.requests[-1].body == {"actionType": "create", "throwACException": False}


async def test_check_object_type_lifecycle_step_security_access(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = "/core/api/security/objectTypes/1031/lifecycleSchemeSteps/5/checkAccess"
    fake_ips.add("post", path, body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_object_type_lifecycle_step_security_access(
            1031, 5, SecurityCheckAccess(action_type="nextLCStep")
        )

    assert result is True
    assert fake_ips.requests[-1].path == path
    assert fake_ips.requests[-1].body == {"actionType": "nextLCStep", "throwACException": False}


async def test_check_object_type_lifecycle_step_attribute_security_access(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = "/core/api/security/objectTypes/1031/lifecycleSchemeSteps/5/attributes/1029/checkAccess"
    fake_ips.add("post", path, body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_object_type_lifecycle_step_attribute_security_access(
            1031, 5, 1029, SecurityCheckAccess(action_type="edit")
        )

    assert result is True
    assert fake_ips.requests[-1].path == path
    assert fake_ips.requests[-1].body == {"actionType": "edit", "throwACException": False}


async def test_check_object_security_access(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/objects/204931/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_object_security_access(
            204931, SecurityCheckAccess(action_type="edit")
        )

    assert result is True
    assert fake_ips.requests[-1].path == "/core/api/security/objects/204931/checkAccess"
    assert fake_ips.requests[-1].body == {"actionType": "edit", "throwACException": False}


async def test_check_relation_types_security_access(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/relationTypes/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_relation_types_security_access(
            SecurityCheckAccess(action_type="read")
        )

    assert result is True
    assert fake_ips.requests[-1].path == "/core/api/security/relationTypes/checkAccess"


async def test_check_relation_type_security_access(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/relationTypes/12/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_relation_type_security_access(
            12, SecurityCheckAccess(action_type="addLink")
        )

    assert result is True
    assert fake_ips.requests[-1].path == "/core/api/security/relationTypes/12/checkAccess"


async def test_check_subject_areas_security_access(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/security/subjectAreas/checkAccess", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_subject_areas_security_access(
            SecurityCheckAccess(action_type="read")
        )

    assert result is True
    assert fake_ips.requests[-1].path == "/core/api/security/subjectAreas/checkAccess"
