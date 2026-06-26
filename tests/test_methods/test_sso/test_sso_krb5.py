"""Тесты метода Kerberos/SSO-аутентификации (sso_krb5_authenticate).

Проверяют путь, тело (передаётся как есть) и распаковку ответа (dict как есть)
на поддельном сервере.
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient

_TOKENS = {
    "accessToken": "acc-krb",
    "refreshToken": "ref-krb",
    "expireTime": "2026-06-25T10:00:00Z",
}


async def test_sso_krb5_authenticate_posts_body_and_returns_tokens(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/sso/krb5/authenticate", body=_TOKENS)
    payload = {"roleID": 10, "accessLevelID": 0}
    async with _Client(config=token_config) as ips:
        tokens = await ips.sso_krb5_authenticate(payload)

    assert tokens == _TOKENS
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/sso/krb5/authenticate"
    assert request.body == payload


async def test_sso_krb5_authenticate_non_dict_returns_empty(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/sso/krb5/authenticate", body=42)
    async with _Client(config=token_config) as ips:
        tokens = await ips.sso_krb5_authenticate({"roleID": 10, "accessLevelID": 0})

    assert tokens == {}
