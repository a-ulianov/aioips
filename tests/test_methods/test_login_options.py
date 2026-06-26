"""Тест метода получения опций входа."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig


async def test_login_options_returns_roles_and_levels(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/Auth/logins/your-login/options",
        body={
            "roles": [{"id": 10, "name": "Администратор"}],
            "accessLevels": [{"id": 0, "name": "Обычный"}],
        },
    )
    async with IPSClient(config=token_config) as ips:
        options = await ips.login_options("your-login")

    assert options.roles[0].id == 10
    assert options.roles[0].name == "Администратор"
    assert options.access_levels[0].name == "Обычный"
