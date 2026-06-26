"""Тесты публичных методов токенов раздела Auth (authenticate/refresh/clone).

Проверяют путь, тело (передаётся как есть) и распаковку ответа (dict как есть)
на поддельном сервере. Без confirm-гейтов — это получение токенов.
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient

_TOKENS = {
    "accessToken": "acc-1",
    "refreshToken": "ref-1",
    "expireTime": "2026-06-25T10:00:00Z",
}


async def test_authenticate_posts_body_and_returns_tokens(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/Auth/authenticate", body=_TOKENS)
    payload = {
        "loginName": "your-login",
        "password": "secret",
        "passwordType": 0,
        "roleID": 10,
        "accessLevelID": 0,
    }
    async with _Client(config=token_config) as ips:
        tokens = await ips.authenticate(payload)

    assert tokens == _TOKENS
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/Auth/authenticate"
    assert request.body == payload


async def test_authenticate_non_dict_returns_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/Auth/authenticate", body=[1, 2, 3])
    async with _Client(config=token_config) as ips:
        tokens = await ips.authenticate({"loginName": "your-login"})

    assert tokens == {}


async def test_refresh_tokens_posts_body_and_returns_tokens(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fresh = {"accessToken": "acc-2", "refreshToken": "ref-2", "expireTime": None}
    fake_ips.add("post", "/core/api/Auth/refreshTokens", body=fresh)
    async with _Client(config=token_config) as ips:
        result = await ips.refresh_tokens(_TOKENS)

    assert result == fresh
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/Auth/refreshTokens"
    assert request.body == _TOKENS


async def test_clone_tokens_posts_body_and_returns_pairs(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    cloned = {"primaryPair": _TOKENS, "secondaryPair": _TOKENS}
    fake_ips.add("post", "/core/api/Auth/cloneTokens", body=cloned)
    async with _Client(config=token_config) as ips:
        result = await ips.clone_tokens(_TOKENS)

    assert result == cloned
    assert result["secondaryPair"]["accessToken"] == "acc-1"
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/Auth/cloneTokens"
    assert request.body == _TOKENS
