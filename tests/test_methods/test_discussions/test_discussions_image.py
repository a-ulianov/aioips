"""Тесты мутирующего метода загрузки изображения в обсуждение (multipart)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient

_RESULT = {
    "objectVersionGuid": "cad001c5-306c-11d8-b4e9-00304f19f545",
    "fileName": "shot.png",
}


async def test_add_discussion_image_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.add_discussion_image(b"png", "shot.png", object_version_id=102550)

    assert fake_ips.requests == []


async def test_add_discussion_image_sends_query_and_unpacks(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/discussions/addImage", body=_RESULT)
    async with _Client(config=token_config) as ips:
        result = await ips.add_discussion_image(
            b"\x89PNG",
            "shot.png",
            discussion_version_id=7001,
            object_version_id=102550,
            confirm=True,
        )

    assert result["fileName"] == "shot.png"
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/discussions/addImage"
    assert request.query["discussionVersionId"] == "7001"
    assert request.query["objectVersionId"] == "102550"


async def test_add_discussion_image_omits_unset_query(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/discussions/addImage", body=_RESULT)
    async with _Client(config=token_config) as ips:
        await ips.add_discussion_image(b"x", "x", object_version_id=102550, confirm=True)

    request = fake_ips.requests[-1]
    assert request.query["objectVersionId"] == "102550"
    assert "discussionVersionId" not in request.query


async def test_add_discussion_image_non_dict_to_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/discussions/addImage", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.add_discussion_image(b"x", "x", confirm=True)

    assert result == {}
