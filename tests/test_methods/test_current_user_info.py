"""Тест метода информации о текущем пользователе."""

from uuid import UUID

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig


async def test_current_user_info_parses_session(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/currentUsers/userInfo",
        body={
            "sessionId": "5e0e17a8-16ab-49f1-bcd0-7530d4d1b042",
            "userVersionId": 4,
            "userName": "Системный администратор",
            "roleVersionId": 10,
            "accessLevel": 0,
            "isAdmin": True,
            "loginName": "your-login",
        },
    )
    async with IPSClient(config=token_config) as ips:
        info = await ips.user_info()

    assert info.login_name == "your-login"
    assert info.is_admin is True
    assert info.user_name == "Системный администратор"
    assert info.session_id == UUID("5e0e17a8-16ab-49f1-bcd0-7530d4d1b042")
