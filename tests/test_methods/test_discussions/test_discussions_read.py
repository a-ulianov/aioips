"""Тесты методов чтения раздела обсуждений (discussions)."""

from datetime import datetime
from uuid import UUID

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
    "curiousUsers": ["cad001c5-306c-11d8-b4e9-00304f19f546"],
    "context": {
        "objectVersionGuidToCaptionMap": [
            {
                "item1": "cad001c5-306c-11d8-b4e9-00304f19f547",
                "item2": "Деталь 12.345",
            }
        ]
    },
    "isReadOnly": False,
    "isReplyOnly": True,
}


async def test_can_discuss_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/discussions/canDiscuss", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.can_discuss(102550)

    assert result is True
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/discussions/canDiscuss"


async def test_get_messages_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/discussions/getMessages", body=[_MESSAGE])
    async with IPSClient(config=token_config) as ips:
        messages = await ips.get_messages([_MESSAGE_ID])

    assert len(messages) == 1
    msg = messages[0]
    assert msg.id.discussion_version_id == 7001
    assert msg.id.creation_timestamp == datetime.fromisoformat("2026-06-24T09:30:00+00:00")
    assert msg.id.author_version_guid == UUID("cad001c5-306c-11d8-b4e9-00304f19f545")
    assert msg.author_name == "Иванов И.И."
    assert msg.caption == "Замечание по чертежу"
    assert msg.last_modification_timestamp == datetime.fromisoformat("2026-06-24T10:15:00+00:00")
    assert msg.text == "Проверьте размеры на листе 2."
    assert msg.curious_users == [UUID("cad001c5-306c-11d8-b4e9-00304f19f546")]
    assert msg.is_read_only is False
    assert msg.is_reply_only is True
    tuple_ = msg.context.object_version_guid_to_caption_map[0]
    assert tuple_.item1 == UUID("cad001c5-306c-11d8-b4e9-00304f19f547")
    assert tuple_.item2 == "Деталь 12.345"


async def test_get_messages_coerces_null_lists(token_config: IPSConfig, fake_ips: FakeIPS):
    message = {**_MESSAGE, "curiousUsers": None}
    fake_ips.add("get", "/core/api/discussions/getMessages", body=[message])
    async with IPSClient(config=token_config) as ips:
        messages = await ips.get_messages([_MESSAGE_ID])

    assert messages[0].curious_users == []


async def test_get_messages_by_id_uses_path(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/discussions/7001/getMessagesById",
        body=[_MESSAGE],
    )
    async with IPSClient(config=token_config) as ips:
        messages = await ips.get_messages_by_id(7001)

    assert len(messages) == 1
    assert messages[0].id.discussion_version_id == 7001
    assert fake_ips.requests[-1].path == "/core/api/discussions/7001/getMessagesById"


async def test_find_messages_passes_all_versions_flag(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/discussions/102550/findMessages",
        body=[_MESSAGE],
    )
    async with IPSClient(config=token_config) as ips:
        messages = await ips.find_messages(102550, all_object_versions=True)

    assert len(messages) == 1
    assert messages[0].caption == "Замечание по чертежу"
    assert fake_ips.requests[-1].path == "/core/api/discussions/102550/findMessages"
