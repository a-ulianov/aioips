"""Тесты восстановления доступа администратора (restoreAdminAccess) и новых checkAccess.

Группа A (``restore_admin_access_*`` / ``restore_object_type_...``) — мутации без тела:
проверяем confirm-гейт (``confirm=False`` → :class:`ValueError`, запрос НЕ выполняется),
а при ``confirm=True`` — корректный путь POST, пустое тело ``{}`` и возврат ``None``.

Группа B (``check_*``) — read-проверки с телом ``CheckAccessDto``: путь, сериализация
тела с алиасами и интерпретация ``boolean``-ответа в ``bool``.
"""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.security import SecurityCheckAccess

_Client = IPSClient


# --------------------------------------------------------------------------- #
# Группа A — restoreAdminAccess: коллекции (без параметров пути)                #
# --------------------------------------------------------------------------- #
async def test_restore_actions_on_objects_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.restore_admin_access_actions_on_objects()

    assert fake_ips.requests == []  # запрос не выполнялся


async def test_restore_actions_on_objects(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/actionOnObjects/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.restore_admin_access_actions_on_objects(confirm=True)

    assert result is None
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == path
    assert req.body == {}


async def test_restore_attribute_groups(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/attributeGroups/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.restore_admin_access_attribute_groups(confirm=True) is None
    assert fake_ips.requests[-1].path == path
    assert fake_ips.requests[-1].body == {}


async def test_restore_attributes(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/attributes/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.restore_admin_access_attributes(confirm=True) is None
    assert fake_ips.requests[-1].path == path


async def test_restore_languages(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/languages/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.restore_admin_access_languages(confirm=True) is None
    assert fake_ips.requests[-1].path == path


async def test_restore_lifecycle_levels(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/lifecycleLevels/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.restore_admin_access_lifecycle_levels(confirm=True) is None
    assert fake_ips.requests[-1].path == path


async def test_restore_lifecycle_schemes(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/lifecycleSchemes/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.restore_admin_access_lifecycle_schemes(confirm=True) is None
    assert fake_ips.requests[-1].path == path


async def test_restore_object_types(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/objectTypes/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.restore_admin_access_object_types(confirm=True) is None
    assert fake_ips.requests[-1].path == path


async def test_restore_relation_types(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/relationTypes/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.restore_admin_access_relation_types(confirm=True) is None
    assert fake_ips.requests[-1].path == path


async def test_restore_subject_areas(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/subjectAreas/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.restore_admin_access_subject_areas(confirm=True) is None
    assert fake_ips.requests[-1].path == path


async def test_restore_system(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/system/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.restore_admin_access_system(confirm=True) is None
    assert fake_ips.requests[-1].path == path


# --------------------------------------------------------------------------- #
# Группа A — restoreAdminAccess: одиночные цели (с параметрами пути)            #
# --------------------------------------------------------------------------- #
async def test_restore_attribute_group(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/attributeGroups/42/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.restore_admin_access_attribute_group(42, confirm=True) is None
    assert fake_ips.requests[-1].path == path
    assert fake_ips.requests[-1].body == {}


async def test_restore_attribute_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.restore_admin_access_attribute(1029)
    assert fake_ips.requests == []


async def test_restore_attribute(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/attributes/1029/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.restore_admin_access_attribute(1029, confirm=True) is None
    assert fake_ips.requests[-1].path == path


async def test_restore_lifecycle_level(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/lifecycleLevels/3/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.restore_admin_access_lifecycle_level(3, confirm=True) is None
    assert fake_ips.requests[-1].path == path


async def test_restore_lifecycle_scheme(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/lifecycleSchemes/7/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.restore_admin_access_lifecycle_scheme(7, confirm=True) is None
    assert fake_ips.requests[-1].path == path


async def test_restore_object_type(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/objectTypes/1031/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.restore_admin_access_object_type(1031, confirm=True) is None
    assert fake_ips.requests[-1].path == path
    assert fake_ips.requests[-1].body == {}


async def test_restore_object_type_lifecycle_scheme_step(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = "/core/api/security/objectTypes/1031/lifecycleSchemeSteps/5/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.restore_admin_access_object_type_lifecycle_scheme_step(
            1031, 5, confirm=True
        )
    assert result is None
    assert fake_ips.requests[-1].path == path


async def test_restore_object_type_lifecycle_scheme_step_for_attribute(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = (
        "/core/api/security/objectTypes/1031/lifecycleSchemeSteps/5"
        "/attributes/1029/restoreAdminAccess"
    )
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.restore_object_type_lifecycle_scheme_step_for_attribute(
            1031, 5, 1029, confirm=True
        )
    assert result is None
    assert fake_ips.requests[-1].path == path
    assert fake_ips.requests[-1].body == {}


async def test_restore_object(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/objects/204931/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.restore_admin_access_object(204931, confirm=True) is None
    assert fake_ips.requests[-1].path == path


async def test_restore_relation_type(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/relationTypes/12/restoreAdminAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.restore_admin_access_relation_type(12, confirm=True) is None
    assert fake_ips.requests[-1].path == path


# --------------------------------------------------------------------------- #
# Группа B — новые checkAccess (read, с телом, → bool)                          #
# --------------------------------------------------------------------------- #
async def test_check_lifecycle_step_attribute_access_true(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = "/core/api/security/objectTypes/1031/lifecycleSchemeSteps/5/attributes/1029/checkAccess"
    fake_ips.add("post", path, body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_object_type_lifecycle_scheme_step_access_for_attribute(
            1031, 5, 1029, SecurityCheckAccess(action_type="edit")
        )

    assert result is True
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == path
    assert req.body == {"actionType": "edit", "throwACException": False}


async def test_check_lifecycle_step_attribute_access_false(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = "/core/api/security/objectTypes/1031/lifecycleSchemeSteps/5/attributes/1029/checkAccess"
    fake_ips.add("post", path, body=False)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_object_type_lifecycle_scheme_step_access_for_attribute(
            1031, 5, 1029, SecurityCheckAccess(action_type="edit")
        )
    assert result is False


async def test_check_lifecycle_step_attribute_access_none_is_false(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = "/core/api/security/objectTypes/1031/lifecycleSchemeSteps/5/attributes/1029/checkAccess"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_object_type_lifecycle_scheme_step_access_for_attribute(
            1031, 5, 1029, SecurityCheckAccess(action_type="edit")
        )
    assert result is False  # fail-closed


async def test_check_update_lifecycle_step_access_true(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/objectTypes/1031/lifecycleSchemeSteps/5/checkAccess"
    fake_ips.add("post", path, body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.check_update_object_type_lifecycle_scheme_step_access(
            1031, 5, SecurityCheckAccess(action_type="setAccess")
        )

    assert result is True
    req = fake_ips.requests[-1]
    assert req.path == path
    assert req.body == {"actionType": "setAccess", "throwACException": False}


async def test_check_update_lifecycle_step_access_aliases(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    """Все поля DTO уходят под camelCase-алиасами; ``None`` исключается."""
    path = "/core/api/security/objectTypes/1031/lifecycleSchemeSteps/5/checkAccess"
    fake_ips.add("post", path, body=True)
    async with IPSClient(config=token_config) as ips:
        await ips.check_update_object_type_lifecycle_scheme_step_access(
            1031,
            5,
            SecurityCheckAccess(
                action_type="setAccess", default_access=True, throw_ac_exception=True
            ),
        )

    assert fake_ips.requests[-1].body == {
        "actionType": "setAccess",
        "defaultAccess": True,
        "throwACException": True,
    }
