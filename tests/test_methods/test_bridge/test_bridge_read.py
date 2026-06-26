"""Тесты методов чтения раздела IPS Bridge."""

from uuid import UUID

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_USER = {
    "id": 7,
    "userName": "Иванов И.И.",
    "loginName": "ivanov",
    "databaseId": "DB-01",
}

_PLUGIN = {
    "objectId": 1001,
    "pluginName": "PdfViewer",
    "assemblyName": "Intermech.Pdf",
    "assemblyVersion": "9.0.1.0",
}

_ACTION = {
    "actionId": "cad001c5-306c-11d8-b4e9-00304f19f545",
    "handlerId": "cad001c5-306c-11d8-b4e9-00304f19f546",
    "displayName": "Открыть в просмотрщике",
}


async def test_bridge_common_settings(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Bridge/commonSettings", body={"ipsBridgePort": 12345})
    async with IPSClient(config=token_config) as ips:
        settings = await ips.bridge_common_settings()

    assert settings.ips_bridge_port == 12345


async def test_bridge_common_settings_defaults_port(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Bridge/commonSettings", body={})
    async with IPSClient(config=token_config) as ips:
        settings = await ips.bridge_common_settings()

    assert settings.ips_bridge_port == 0


async def test_bridge_user_info(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Bridge/UserInfo", body=_USER)
    async with IPSClient(config=token_config) as ips:
        user = await ips.bridge_user_info()

    assert user.id == 7
    assert user.user_name == "Иванов И.И."
    assert user.login_name == "ivanov"
    assert user.database_id == "DB-01"


async def test_bridge_user_info_nullable_fields(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/Bridge/UserInfo",
        body={"id": 3, "userName": None, "loginName": None, "databaseId": None},
    )
    async with IPSClient(config=token_config) as ips:
        user = await ips.bridge_user_info()

    assert user.id == 3
    assert user.user_name is None
    assert user.login_name is None
    assert user.database_id is None


async def test_bridge_plugins(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Bridge/GetPlugins", body=[_PLUGIN, _PLUGIN])
    async with IPSClient(config=token_config) as ips:
        plugins = await ips.bridge_plugins()

    assert len(plugins) == 2
    plugin = plugins[0]
    assert plugin.object_id == 1001
    assert plugin.plugin_name == "PdfViewer"
    assert plugin.assembly_name == "Intermech.Pdf"
    assert plugin.assembly_version == "9.0.1.0"


async def test_bridge_plugins_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Bridge/GetPlugins", body=[])
    async with IPSClient(config=token_config) as ips:
        plugins = await ips.bridge_plugins()

    assert plugins == []


async def test_bridge_settings_xml_with_guid(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Bridge/Integrators/GetSettingsXml", body="<settings/>")
    async with IPSClient(config=token_config) as ips:
        xml = await ips.bridge_settings_xml(integrator_guid="abc")

    assert xml == "<settings/>"
    request = fake_ips.requests[-1]
    assert request.query["integratorGuid"] == "abc"


async def test_bridge_settings_xml_without_guid(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Bridge/Integrators/GetSettingsXml", body=None)
    async with IPSClient(config=token_config) as ips:
        xml = await ips.bridge_settings_xml()

    assert xml == ""
    request = fake_ips.requests[-1]
    assert "integratorGuid" not in request.query


async def test_bridge_user_defined_launch_action(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Bridge/Launch/GetUserDefinedLaunchAction", body=_ACTION)
    async with IPSClient(config=token_config) as ips:
        action = await ips.bridge_user_defined_launch_action(object_type_id=1, launch_type=0)

    assert action.action_id == UUID("cad001c5-306c-11d8-b4e9-00304f19f545")
    assert action.handler_id == UUID("cad001c5-306c-11d8-b4e9-00304f19f546")
    assert action.display_name == "Открыть в просмотрщике"
    request = fake_ips.requests[-1]
    assert request.query["objectTypeId"] == "1"
    assert request.query["launchType"] == "0"


async def test_bridge_user_defined_launch_action_omits_unset(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/Bridge/Launch/GetUserDefinedLaunchAction", body=_ACTION)
    async with IPSClient(config=token_config) as ips:
        await ips.bridge_user_defined_launch_action()

    request = fake_ips.requests[-1]
    assert "objectTypeId" not in request.query
    assert "launchType" not in request.query


async def test_bridge_launch_action_info(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Bridge/Launch/GetLaunchActionInfo", body=_ACTION)
    async with IPSClient(config=token_config) as ips:
        action = await ips.bridge_launch_action_info(action_id="some-guid")

    assert action.action_id == UUID("cad001c5-306c-11d8-b4e9-00304f19f545")
    assert action.display_name == "Открыть в просмотрщике"
    request = fake_ips.requests[-1]
    assert request.query["actionId"] == "some-guid"


async def test_bridge_launch_action_data(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Bridge/Launch/GetLaunchActionData", body="payload-xml")
    async with IPSClient(config=token_config) as ips:
        data = await ips.bridge_launch_action_data(action_id="some-guid")

    assert data == "payload-xml"
    request = fake_ips.requests[-1]
    assert request.query["actionId"] == "some-guid"


async def test_bridge_launch_action_data_none_to_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Bridge/Launch/GetLaunchActionData", body=None)
    async with IPSClient(config=token_config) as ips:
        data = await ips.bridge_launch_action_data()

    assert data == ""
