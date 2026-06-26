"""Тесты метода проверки применимости настроек к архиву (чтение через POST)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.archives.permitted_document_types import PermittedDocumentTypes

_Client = IPSClient


async def test_archive_can_apply_settings_posts_body_and_returns_true(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/archives/1029/canApplySettings", body=True)
    body = PermittedDocumentTypes(documents_types=[1742, 1801], types_using_mode="white")
    async with _Client(config=token_config) as ips:
        result = await ips.archive_can_apply_settings(1029, body)

    assert result is True
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/archives/1029/canApplySettings"
    assert request.body == {
        "documentsTypes": [1742, 1801],
        "typesUsingMode": "white",
    }


async def test_archive_can_apply_settings_returns_false(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/archives/1029/canApplySettings", body=False)
    async with _Client(config=token_config) as ips:
        result = await ips.archive_can_apply_settings(1029, PermittedDocumentTypes())

    assert result is False


async def test_archive_can_apply_settings_coerces_truthy(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/archives/7/canApplySettings", body=1)
    async with _Client(config=token_config) as ips:
        result = await ips.archive_can_apply_settings(7, PermittedDocumentTypes())

    assert result is True
