"""Тесты методов чтения раздела ЭЦП (криптографической подписи)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.crypto_signing import CryptoProviderInfo

_SETTINGS = {
    "doRevocation": True,
    "revocationMode": 1,
    "signsDeveloperMode": False,
}


async def test_object_encoded_hash_returns_string(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/cryptoSigning/objectEncodedHash", body="ABCD1234==")
    provider = CryptoProviderInfo(provider_type=75, key_number=1)
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_encoded_hash(102550, "default", 1, provider)

    assert result == "ABCD1234=="


async def test_sign_info_stream_returns_string(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/cryptoSigning/signInfoStream", body="<signs/>")
    async with IPSClient(config=token_config) as ips:
        result = await ips.sign_info_stream(102550, "default")

    assert result == "<signs/>"


async def test_sign_info_stream_null_returns_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    # Объект без подписей: сервер отвечает 200 с пустым телом (null) — не строкой "None".
    fake_ips.add("get", "/core/api/cryptoSigning/signInfoStream", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.sign_info_stream(102550, "default")

    assert result == ""


async def test_signing_settings_returns_dto(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/cryptoSigning/signingSettings", body=_SETTINGS)
    async with IPSClient(config=token_config) as ips:
        settings = await ips.signing_settings()

    assert settings.do_revocation is True
    assert settings.revocation_mode == 1
    assert settings.signs_developer_mode is False


async def test_signing_settings_defaults_on_empty_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/cryptoSigning/signingSettings", body={})
    async with IPSClient(config=token_config) as ips:
        settings = await ips.signing_settings()

    assert settings.do_revocation is False
    assert settings.revocation_mode == 0
    assert settings.signs_developer_mode is False
