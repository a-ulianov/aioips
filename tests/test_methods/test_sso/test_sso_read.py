"""Тесты методов чтения раздела Single Sign-On (SSO)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_OPTIONS = {
    "loginName": "DOMAIN\\ivanov",
    "loginOptions": {
        "roles": [{"id": 10, "name": "Конструктор"}],
        "accessLevels": [{"id": 1, "name": "Общий"}],
    },
}


async def test_kerberos_auth_options_returns_dto(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/sso/krb5/currentUser/options", body=_OPTIONS)
    async with IPSClient(config=token_config) as ips:
        options = await ips.kerberos_auth_options()

    assert options.login_name == "DOMAIN\\ivanov"
    assert len(options.login_options.roles) == 1
    assert options.login_options.roles[0].id == 10
    assert options.login_options.roles[0].name == "Конструктор"
    assert options.login_options.access_levels[0].id == 1
    assert options.login_options.access_levels[0].name == "Общий"


async def test_kerberos_auth_options_coerces_null_lists(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {"loginName": "DOMAIN\\petrov", "loginOptions": {"roles": None, "accessLevels": None}}
    fake_ips.add("get", "/core/api/sso/krb5/currentUser/options", body=body)
    async with IPSClient(config=token_config) as ips:
        options = await ips.kerberos_auth_options()

    assert options.login_name == "DOMAIN\\petrov"
    assert options.login_options.roles == []
    assert options.login_options.access_levels == []
