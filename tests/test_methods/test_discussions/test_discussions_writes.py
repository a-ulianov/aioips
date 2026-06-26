"""Тесты мутирующих методов раздела обсуждений (discussions)."""

from datetime import datetime
from uuid import UUID

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.discussions import MessageId

_MESSAGE_ID = MessageId(
    discussion_version_id=7001,
    creation_timestamp=datetime.fromisoformat("2026-06-24T09:30:00+00:00"),
    author_version_guid=UUID("cad001c5-306c-11d8-b4e9-00304f19f545"),
)

_MESSAGE = {
    "id": {
        "discussionVersionId": 7001,
        "creationTimestamp": "2026-06-24T09:30:00Z",
        "authorVersionGuid": "cad001c5-306c-11d8-b4e9-00304f19f545",
    },
    "authorName": "Иванов И.И.",
    "caption": "Замечание по чертежу",
    "lastModificationTimestamp": "2026-06-24T10:15:00Z",
    "text": "Проверьте размеры на листе 2.",
    "curiousUsers": [],
    "context": {"objectVersionGuidToCaptionMap": []},
    "isReadOnly": False,
    "isReplyOnly": False,
}


async def test_add_message_uses_query_and_empty_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/discussions/addMessage", body=_MESSAGE)
    async with IPSClient(config=token_config) as ips:
        message = await ips.add_message(
            102550,
            caption="Замечание по чертежу",
            text="Проверьте размеры на листе 2.",
        )

    assert message.id.discussion_version_id == 7001
    assert message.caption == "Замечание по чертежу"
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/discussions/addMessage"
    assert request.body == {}
    assert request.query["objectVersionId"] == "102550"
    assert request.query["caption"] == "Замечание по чертежу"
    assert request.query["text"] == "Проверьте размеры на листе 2."


async def test_add_message_omits_unset_query_params(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/discussions/addMessage", body=_MESSAGE)
    async with IPSClient(config=token_config) as ips:
        await ips.add_message(102550, text="Только текст")

    request = fake_ips.requests[-1]
    assert request.query["objectVersionId"] == "102550"
    assert request.query["text"] == "Только текст"
    assert "caption" not in request.query


async def test_edit_message_sends_message_id_body_and_query(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/discussions/editMessage", body=_MESSAGE)
    async with IPSClient(config=token_config) as ips:
        message = await ips.edit_message(_MESSAGE_ID, text="Уточнено.")

    assert message.id.discussion_version_id == 7001
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/discussions/editMessage"
    assert request.body == {
        "discussionVersionId": 7001,
        "creationTimestamp": "2026-06-24T09:30:00Z",
        "authorVersionGuid": "cad001c5-306c-11d8-b4e9-00304f19f545",
    }
    assert request.query["text"] == "Уточнено."
    assert "caption" not in request.query


async def test_remove_message_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.remove_message(_MESSAGE_ID)

    assert fake_ips.requests == []


async def test_remove_message_sends_body_and_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/discussions/removeMessage", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.remove_message(_MESSAGE_ID, confirm=True)

    assert result is True
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/discussions/removeMessage"
    assert request.body == {
        "discussionVersionId": 7001,
        "creationTimestamp": "2026-06-24T09:30:00Z",
        "authorVersionGuid": "cad001c5-306c-11d8-b4e9-00304f19f545",
    }


async def test_remove_message_false_on_empty_response(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/discussions/removeMessage", body=False)
    async with IPSClient(config=token_config) as ips:
        result = await ips.remove_message(_MESSAGE_ID, confirm=True)

    assert result is False
