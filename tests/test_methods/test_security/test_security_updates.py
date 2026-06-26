"""Тесты мутирующих методов установки прав доступа (Группа C — Update*/childTargets).

Каждый метод проверяется на трёх уровнях:
- confirm-гейт: ``confirm=False`` → :class:`ValueError`, запрос НЕ выполняется;
- запись модели :class:`Security`: ``confirm=True`` → корректный путь, тело
  сериализуется ``by_alias`` + ``exclude_none``, возврат ``None``;
- запись «сырого» ``dict``: тело уходит как есть (round-trip write-same-back).
"""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.security import PermissionAction, Security, SecurityTarget

_Client = IPSClient


def _security_model() -> Security:
    return Security(
        targets=[SecurityTarget(target_id=7, target_name="Конструкторы")],
        permissions=[PermissionAction(action_id="read", target_id=7, access_type="grant")],
    )


_SECURITY_DICT = {
    "targets": [{"targetId": 7, "targetName": "Конструкторы"}],
    "permissions": [{"actionId": "read", "targetId": 7, "accessType": "grant"}],
    "isConditionsEnabled": False,
}


# --------------------------------------------------------------------------- #
# update_object_type_security_child_targets                                     #
# --------------------------------------------------------------------------- #
async def test_update_object_type_child_targets_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.update_object_type_security_child_targets(1031, _security_model())
    assert fake_ips.requests == []


async def test_update_object_type_child_targets_model(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/objectTypes/1031/childTargets"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.update_object_type_security_child_targets(
            1031, _security_model(), confirm=True
        )

    assert result is None
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == path
    assert req.body["targets"][0]["targetId"] == 7  # type: ignore[index]
    assert req.body["targets"][0]["targetName"] == "Конструкторы"  # type: ignore[index]
    assert req.body["permissions"][0]["accessType"] == "grant"  # type: ignore[index]


async def test_update_object_type_child_targets_dict_passthrough(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = "/core/api/security/objectTypes/1031/childTargets"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        await ips.update_object_type_security_child_targets(1031, _SECURITY_DICT, confirm=True)
    assert fake_ips.requests[-1].body == _SECURITY_DICT


# --------------------------------------------------------------------------- #
# update_object_type_lifecycle_scheme_step_security                             #
# --------------------------------------------------------------------------- #
async def test_update_lifecycle_step_security_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.update_object_type_lifecycle_scheme_step_security(1031, 5, _security_model())
    assert fake_ips.requests == []


async def test_update_lifecycle_step_security_model(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/objectTypes/1031/lifecycleSchemeSteps/5"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.update_object_type_lifecycle_scheme_step_security(
            1031, 5, _security_model(), confirm=True
        )

    assert result is None
    assert fake_ips.requests[-1].path == path
    assert fake_ips.requests[-1].body["targets"][0]["targetId"] == 7  # type: ignore[index]


async def test_update_lifecycle_step_security_dict_with_apply_to_childs(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    """``isNeedToApplyToChilds`` доступен только через dict (нет в схеме Security)."""
    path = "/core/api/security/objectTypes/1031/lifecycleSchemeSteps/5"
    fake_ips.add("post", path, body=None)
    body = {**_SECURITY_DICT, "isNeedToApplyToChilds": True}
    async with IPSClient(config=token_config) as ips:
        await ips.update_object_type_lifecycle_scheme_step_security(1031, 5, body, confirm=True)
    assert fake_ips.requests[-1].body == body


# --------------------------------------------------------------------------- #
# update_object_type_lifecycle_scheme_step_security_for_attribute               #
# --------------------------------------------------------------------------- #
async def test_update_lifecycle_step_attribute_security_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.update_object_type_lifecycle_scheme_step_security_for_attribute(
                1031, 5, 1029, _security_model()
            )
    assert fake_ips.requests == []


async def test_update_lifecycle_step_attribute_security_model(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = "/core/api/security/objectTypes/1031/lifecycleSchemeSteps/5/attributes/1029"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.update_object_type_lifecycle_scheme_step_security_for_attribute(
            1031, 5, 1029, _security_model(), confirm=True
        )

    assert result is None
    assert fake_ips.requests[-1].path == path
    assert fake_ips.requests[-1].body["permissions"][0]["actionId"] == "read"  # type: ignore[index]


# --------------------------------------------------------------------------- #
# update_object_type_lifecycle_scheme_step_child_targets                        #
# --------------------------------------------------------------------------- #
async def test_update_lifecycle_step_child_targets_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.update_object_type_lifecycle_scheme_step_child_targets(
                1031, 5, _security_model()
            )
    assert fake_ips.requests == []


async def test_update_lifecycle_step_child_targets_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/security/objectTypes/1031/lifecycleSchemeSteps/5/childTargets"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.update_object_type_lifecycle_scheme_step_child_targets(
            1031, 5, _SECURITY_DICT, confirm=True
        )
    assert result is None
    assert fake_ips.requests[-1].path == path
    assert fake_ips.requests[-1].body == _SECURITY_DICT
