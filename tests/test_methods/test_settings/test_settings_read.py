"""Тесты методов чтения раздела настроек (settings)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.settings import ToolSecurityGroup, ToolSecurityRights


async def test_security_data_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    body = [
        {"userId": 500, "securityGroup": "administrator"},
        {"userId": 12, "securityGroup": "normalUser"},
    ]
    fake_ips.add("post", "/core/api/settings/getSecurityData", body=body)
    async with IPSClient(config=token_config) as ips:
        records = await ips.security_data()

    assert len(records) == 2
    assert records[0].user_id == 500
    assert records[0].security_group is ToolSecurityGroup.ADMINISTRATOR
    assert records[1].security_group is ToolSecurityGroup.NORMAL_USER
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/settings/getSecurityData"
    assert req.body == {}


async def test_security_data_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/settings/getSecurityData", body=[])
    async with IPSClient(config=token_config) as ips:
        records = await ips.security_data()

    assert records == []


async def test_security_data_null_group(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/settings/getSecurityData",
        body=[{"userId": 7, "securityGroup": None}],
    )
    async with IPSClient(config=token_config) as ips:
        records = await ips.security_data()

    assert records[0].user_id == 7
    assert records[0].security_group is None


async def test_user_group_returns_enum(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/settings/getUserGroup", body="restrictedUser")
    async with IPSClient(config=token_config) as ips:
        group = await ips.user_group()

    assert group is ToolSecurityGroup.RESTRICTED_USER
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/settings/getUserGroup"
    assert req.body == {}


async def test_user_rights_returns_enum(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/settings/getUserRights", body="editPublicSettings")
    async with IPSClient(config=token_config) as ips:
        rights = await ips.user_rights()

    assert rights is ToolSecurityRights.EDIT_PUBLIC_SETTINGS
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/settings/getUserRights"
    assert req.body == {}


async def test_view_print_settings_parses(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {
        "injectSigns": True,
        "injectFileChecksum": False,
        "injectedAttributes": {"entity": {"items": [1, 2]}, "isEntityPresent": True},
    }
    fake_ips.add("post", "/core/api/settings/view/1742/getSettings", body=body)
    async with IPSClient(config=token_config) as ips:
        settings = await ips.view_print_settings(1742)

    assert settings.inject_signs is True
    assert settings.inject_file_checksum is False
    assert settings.injected_attributes == {
        "entity": {"items": [1, 2]},
        "isEntityPresent": True,
    }
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/settings/view/1742/getSettings"
    assert req.body == {}


async def test_view_print_settings_tristate_none(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {
        "injectSigns": None,
        "injectFileChecksum": None,
        "injectedAttributes": None,
    }
    fake_ips.add("post", "/core/api/settings/view/1031/getSettings", body=body)
    async with IPSClient(config=token_config) as ips:
        settings = await ips.view_print_settings(1031)

    assert settings.inject_signs is None
    assert settings.inject_file_checksum is None
    assert settings.injected_attributes is None
