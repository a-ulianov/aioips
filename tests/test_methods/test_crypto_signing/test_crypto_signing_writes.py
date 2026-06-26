"""Тесты мутирующих методов раздела ЭЦП (создание подписей)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient

_RESULT = {
    "signedObjectId": 102550,
    "signObjectId": 999001,
    "errorMessage": None,
}


async def test_create_crypto_sign_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.create_crypto_sign({"signedObject": 102550}, eds_as_string="cert")

    assert fake_ips.requests == []


async def test_create_crypto_sign_sends_body_query_and_unpacks(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/cryptoSigning/createCryptoSign", body=_RESULT)
    async with _Client(config=token_config) as ips:
        result = await ips.create_crypto_sign(
            {"signedObject": 102550, "userID": 7},
            eds_as_string="cert-string",
            confirm=True,
        )

    assert result["signObjectId"] == 999001
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/cryptoSigning/createCryptoSign"
    assert request.body == {"signedObject": 102550, "userID": 7}
    assert request.query["edsAsString"] == "cert-string"


async def test_create_separated_crypto_sign_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.create_separated_crypto_sign(102550, {}, eds_as_string="cert")

    assert fake_ips.requests == []


async def test_create_separated_crypto_sign_sends_object_id_query(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/cryptoSigning/createSeparatedCryptoSign", body=_RESULT)
    async with _Client(config=token_config) as ips:
        result = await ips.create_separated_crypto_sign(
            102550,
            {"signedObject": 102550},
            eds_as_string="cert-string",
            confirm=True,
        )

    assert result["signedObjectId"] == 102550
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/cryptoSigning/createSeparatedCryptoSign"
    assert request.body == {"signedObject": 102550}
    assert request.query["objectId"] == "102550"
    assert request.query["edsAsString"] == "cert-string"


async def test_create_crypto_sign_non_dict_to_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/cryptoSigning/createCryptoSign", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.create_crypto_sign({}, eds_as_string="cert", confirm=True)

    assert result == {}
