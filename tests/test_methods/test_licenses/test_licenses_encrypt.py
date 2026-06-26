"""Тесты метода шифрования лицензионных данных (POST-чтение)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.licenses.encrypt import EncryptLicense

_Client = IPSClient

_PATH = "/core/api/licenses/encrypt"


async def test_licenses_encrypt_posts_body_and_returns_string(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", _PATH, body="ENCRYPTED-RESULT")
    payload = EncryptLicense(app_id=42, client_id="client-7", data_as_base64_string="QkFTRTY0")

    async with _Client(config=token_config) as ips:
        result = await ips.licenses_encrypt(payload)

    assert result == "ENCRYPTED-RESULT"

    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == _PATH
    # тело сериализовано с camelCase-алиасами
    assert req.body == {
        "appId": 42,
        "clientId": "client-7",
        "dataAsBase64String": "QkFTRTY0",
    }


async def test_licenses_encrypt_coerces_non_string(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", _PATH, body=12345)
    payload = EncryptLicense(app_id=1, client_id="c", data_as_base64_string="x")

    async with _Client(config=token_config) as ips:
        result = await ips.licenses_encrypt(payload)

    assert result == "12345"
