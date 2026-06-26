"""Тесты методов чтения раздела конфигурации сервера IPS.

Раздел ``config`` пока не включён в :class:`IPSClient`, поэтому тесты используют
минимальный клиент :class:`_ConfigClient` на базе агрегатора :class:`ConfigAPI`
(тот же базовый ``APIManager``, что и у боевого клиента, — реальный путь запроса
проверяется честно).
"""

from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.methods.config import ConfigAPI


class _ConfigClient(ConfigAPI):
    """Тестовый клиент только с методами раздела конфигурации."""


async def test_read_bool_path_and_params(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Config/ReadBool", body=True)
    async with _ConfigClient(config=token_config) as ips:
        result = await ips.config_read_bool(
            module_name="Core",
            section_id=7,
            param_name="UseCache",
            default_value="false",
            config_mode=2,
        )

    assert result is True
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/Config/ReadBool"
    assert req.query == {
        "moduleName": "Core",
        "sectionID": "7",
        "paramName": "UseCache",
        "defaultValue": "false",
        "configMode": "2",
    }


async def test_read_bool_no_params_empty_query(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Config/ReadBool", body=False)
    async with _ConfigClient(config=token_config) as ips:
        result = await ips.config_read_bool()

    assert result is False
    assert fake_ips.requests[-1].query == {}


async def test_read_bool_null_defaults_false(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Config/ReadBool", body=None)
    async with _ConfigClient(config=token_config) as ips:
        assert await ips.config_read_bool(param_name="x") is False


async def test_read_string_path_and_value(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Config/ReadString", body="X:/vault")
    async with _ConfigClient(config=token_config) as ips:
        result = await ips.config_read_string(module_name="Vault", param_name="RootPath")

    assert result == "X:/vault"
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/Config/ReadString"
    assert req.query == {"moduleName": "Vault", "paramName": "RootPath"}


async def test_read_string_null_is_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Config/ReadString", body=None)
    async with _ConfigClient(config=token_config) as ips:
        assert await ips.config_read_string() == ""
    assert fake_ips.requests[-1].query == {}


async def test_read_integer_coerces(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Config/ReadInteger", body=100)
    async with _ConfigClient(config=token_config) as ips:
        result = await ips.config_read_integer(section_id=3, param_name="MaxConnections")

    assert result == 100
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/Config/ReadInteger"
    assert req.query == {"sectionID": "3", "paramName": "MaxConnections"}


async def test_read_integer_null_defaults_zero(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Config/ReadInteger", body=None)
    async with _ConfigClient(config=token_config) as ips:
        assert await ips.config_read_integer() == 0


async def test_read_double_coerces(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Config/ReadDouble", body=1.5)
    async with _ConfigClient(config=token_config) as ips:
        result = await ips.config_read_double(param_name="ScaleFactor")

    assert result == 1.5
    assert fake_ips.requests[-1].path == "/core/api/Config/ReadDouble"
    assert fake_ips.requests[-1].query == {"paramName": "ScaleFactor"}


async def test_read_double_null_defaults_zero(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Config/ReadDouble", body=None)
    async with _ConfigClient(config=token_config) as ips:
        assert await ips.config_read_double() == 0.0


async def test_read_date_time_returns_iso_string(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Config/ReadDateTime", body="2026-06-24T00:00:00")
    async with _ConfigClient(config=token_config) as ips:
        result = await ips.config_read_date_time(module_name="Core", param_name="LastSync")

    assert result == "2026-06-24T00:00:00"
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/Config/ReadDateTime"
    assert req.query == {"moduleName": "Core", "paramName": "LastSync"}


async def test_read_date_time_null_is_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Config/ReadDateTime", body=None)
    async with _ConfigClient(config=token_config) as ips:
        assert await ips.config_read_date_time() == ""


async def test_read_string_no_cache_serializes_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Config/ReadStringNoCache", body="fresh")
    async with _ConfigClient(config=token_config) as ips:
        result = await ips.config_read_string_no_cache(
            module_name="Vault",
            section_id=1,
            param_name="RootPath",
            is_global_param=True,
        )

    assert result == "fresh"
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/Config/ReadStringNoCache"
    assert req.query == {
        "moduleName": "Vault",
        "sectionID": "1",
        "paramName": "RootPath",
        "isGlobalParam": "true",
    }


async def test_read_string_no_cache_no_params(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Config/ReadStringNoCache", body=None)
    async with _ConfigClient(config=token_config) as ips:
        assert await ips.config_read_string_no_cache() == ""
    assert fake_ips.requests[-1].query == {}


async def test_server_os_platform(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Config/GetServerOsPlatform", body="Windows")
    async with _ConfigClient(config=token_config) as ips:
        result = await ips.server_os_platform()

    assert result == "Windows"
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/Config/GetServerOsPlatform"
    assert req.query == {}


async def test_server_os_platform_null_is_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/Config/GetServerOsPlatform", body=None)
    async with _ConfigClient(config=token_config) as ips:
        assert await ips.server_os_platform() == ""
