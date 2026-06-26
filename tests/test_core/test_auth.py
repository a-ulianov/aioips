"""Тесты менеджера авторизации (жизненный цикл токена, роли, обновление)."""

import logging
from typing import Any

import pytest
from tests.conftest import BASE_URL

from aioips import IPSConfig
from aioips.core.auth import AuthManager
from aioips.core.exceptions import IPSAuthError, IPSError

_LOGGER = logging.getLogger("aioips.test")

_TOKENS_FUTURE = {
    "accessToken": "access-future",
    "refreshToken": "refresh-1",
    "expireTime": "2099-01-01T00:00:00Z",
}
_TOKENS_PAST = {
    "accessToken": "access-past",
    "refreshToken": "refresh-0",
    "expireTime": "2000-01-01T00:00:00Z",
}
_OPTIONS = {"roles": [{"id": 10, "name": "Администратор"}], "accessLevels": []}


class FakeTransport:
    """Заглушка низкоуровневого запроса: отдаёт заранее заданные ответы по очереди."""

    def __init__(self, responses: list[tuple[int, dict[str, Any] | None]]) -> None:
        self._responses = responses
        self.calls: list[tuple[str, str, dict[str, Any] | None]] = []

    async def __call__(
        self, method: str, path: str, json: dict[str, Any] | None
    ) -> tuple[int, dict[str, Any] | None]:
        self.calls.append((method, path, json))
        return self._responses.pop(0)


def _login_config(**extra: Any) -> IPSConfig:
    return IPSConfig(
        base_url=BASE_URL,
        login_name="your-login",
        password="secret",
        _env_file=None,
        **extra,
    )


async def test_authenticate_with_explicit_role_id():
    transport = FakeTransport([(200, _TOKENS_FUTURE)])
    auth = AuthManager(_login_config(role_id=10), transport, _LOGGER)

    token = await auth.ensure_access_token()

    assert token == "access-future"
    method, path, payload = transport.calls[0]
    assert (method, path) == ("post", "/core/api/Auth/authenticate")
    assert payload is not None
    assert payload["roleID"] == 10


async def test_role_name_is_resolved_via_options():
    transport = FakeTransport([(200, _OPTIONS), (200, _TOKENS_FUTURE)])
    auth = AuthManager(_login_config(role_name="Администратор"), transport, _LOGGER)

    await auth.ensure_access_token()

    assert transport.calls[0][1].endswith("/options")
    auth_payload = transport.calls[1][2]
    assert auth_payload is not None
    assert auth_payload["roleID"] == 10


async def test_unknown_role_name_raises():
    transport = FakeTransport([(200, {"roles": [], "accessLevels": []})])
    auth = AuthManager(_login_config(role_name="Несуществующая"), transport, _LOGGER)

    with pytest.raises(IPSAuthError, match="недоступна"):
        await auth.ensure_access_token()


async def test_role_defaults_to_zero_when_unset():
    transport = FakeTransport([(200, _TOKENS_FUTURE)])
    auth = AuthManager(_login_config(), transport, _LOGGER)

    await auth.ensure_access_token()

    assert transport.calls[0][2]["roleID"] == 0


async def test_expired_token_triggers_refresh():
    transport = FakeTransport([(200, _TOKENS_PAST), (200, _TOKENS_FUTURE)])
    auth = AuthManager(_login_config(role_id=10), transport, _LOGGER)

    first = await auth.ensure_access_token()
    second = await auth.ensure_access_token()

    assert first == "access-past"
    assert second == "access-future"
    assert transport.calls[1][1] == "/core/api/Auth/refreshTokens"


async def test_failed_refresh_falls_back_to_reauthentication():
    transport = FakeTransport(
        [(200, _TOKENS_PAST), (401, {"title": "expired"}), (200, _TOKENS_FUTURE)]
    )
    auth = AuthManager(_login_config(role_id=10), transport, _LOGGER)

    await auth.ensure_access_token()
    await auth.ensure_access_token()

    paths = [path for _, path, _ in transport.calls]
    assert paths == [
        "/core/api/Auth/authenticate",
        "/core/api/Auth/refreshTokens",
        "/core/api/Auth/authenticate",
    ]


async def test_authenticate_rejection_raises():
    transport = FakeTransport([(401, {"title": "bad", "detail": "Неверный пароль"})])
    auth = AuthManager(_login_config(role_id=10), transport, _LOGGER)

    with pytest.raises(IPSAuthError, match="Неверный пароль"):
        await auth.ensure_access_token()


async def test_token_only_config_cannot_reauthenticate():
    config = IPSConfig(base_url=BASE_URL, access_token="t", _env_file=None)
    transport = FakeTransport([])
    auth = AuthManager(config, transport, _LOGGER)

    with pytest.raises(IPSAuthError):
        await auth.force_refresh()


async def test_login_options_error_raises():
    transport = FakeTransport([(404, None)])
    auth = AuthManager(_login_config(), transport, _LOGGER)

    with pytest.raises(IPSError):
        await auth.login_options("your-login")
