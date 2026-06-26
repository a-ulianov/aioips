"""Тесты методов демонстрационного раздела (samples).

Проверяют чтения (путь/query/распаковка) и мутации (confirm-гейт, тело/query/
распаковка/void) против поддельного сервера :class:`FakeIPS`.
"""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient

_FULL_MESSAGE = {
    "id": 1,
    "createTime": "2026-06-24T09:30:00Z",
    "lastWriteTime": "2026-06-24T10:15:00Z",
    "text": "привет",
}


# --- Чтения -----------------------------------------------------------------


async def test_messages_returns_list_and_path(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/samples/messages", body=[_FULL_MESSAGE])
    async with _Client(config=token_config) as ips:
        items = await ips.messages()

    assert items == [_FULL_MESSAGE]
    request = fake_ips.requests[-1]
    assert request.method == "GET"
    assert request.path == "/core/api/samples/messages"


async def test_messages_empty_on_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/samples/messages", body=None)
    async with _Client(config=token_config) as ips:
        assert await ips.messages() == []


async def test_message_by_id_path_and_unpack(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/samples/messages/1", body=_FULL_MESSAGE)
    async with _Client(config=token_config) as ips:
        message = await ips.message_by_id(1)

    assert message == _FULL_MESSAGE
    assert fake_ips.requests[-1].path == "/core/api/samples/messages/1"


async def test_messages_by_filter_required_and_optional_query(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/samples/messages/queries/byFilter",
        body=[_FULL_MESSAGE],
    )
    async with _Client(config=token_config) as ips:
        items = await ips.messages_by_filter(
            "привет",
            from_time="2026-01-01T00:00:00Z",
        )

    assert items == [_FULL_MESSAGE]
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/samples/messages/queries/byFilter"
    assert request.query["containsText"] == "привет"
    assert request.query["fromTime"] == "2026-01-01T00:00:00Z"
    assert "toTime" not in request.query


async def test_sample_values_unpacks_object(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/samples/values", body={"text": "Здравствуйте"})
    async with _Client(config=token_config) as ips:
        greeting = await ips.sample_values()

    assert greeting == {"text": "Здравствуйте"}
    assert fake_ips.requests[-1].path == "/core/api/samples/values"


# --- Мутации: confirm-гейт ---------------------------------------------------


async def test_add_message_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.add_sample_message({"id": 0, "text": "x"})
    assert fake_ips.requests == []


async def test_update_message_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.update_message(1, _FULL_MESSAGE)
    assert fake_ips.requests == []


async def test_delete_message_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.delete_message(1)
    assert fake_ips.requests == []


async def test_clear_message_updates_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.clear_message_updates()
    assert fake_ips.requests == []


async def test_update_message_text_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.update_message_text(1, "новый")
    assert fake_ips.requests == []


async def test_update_message_last_write_time_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.update_message_last_write_time(1, "2026-06-25T12:00:00Z")
    assert fake_ips.requests == []


# --- Мутации: confirm=True (путь/тело/query/распаковка) ----------------------


async def test_add_message_sends_body_and_returns_object(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/samples/messages", body=_FULL_MESSAGE)
    async with _Client(config=token_config) as ips:
        created = await ips.add_sample_message({"id": 0, "text": "привет"}, confirm=True)

    assert created == _FULL_MESSAGE
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/samples/messages"
    assert request.body == {"id": 0, "text": "привет"}


async def test_update_message_put_body_and_path(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("put", "/core/api/samples/messages/1", body=_FULL_MESSAGE)
    async with _Client(config=token_config) as ips:
        updated = await ips.update_message(1, _FULL_MESSAGE, confirm=True)

    assert updated == _FULL_MESSAGE
    request = fake_ips.requests[-1]
    assert request.method == "PUT"
    assert request.path == "/core/api/samples/messages/1"
    assert request.body == _FULL_MESSAGE


async def test_delete_message_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("delete", "/core/api/samples/messages/1", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.delete_message(1, confirm=True)

    assert result is None
    request = fake_ips.requests[-1]
    assert request.method == "DELETE"
    assert request.path == "/core/api/samples/messages/1"


async def test_clear_message_updates_empty_body_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/samples/messages/updates/clear", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.clear_message_updates(confirm=True)

    assert result is None
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/samples/messages/updates/clear"
    assert request.body == {}


async def test_update_message_text_query_and_empty_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/samples/messages/1/updates/text",
        body=_FULL_MESSAGE,
    )
    async with _Client(config=token_config) as ips:
        updated = await ips.update_message_text(1, "новый текст", confirm=True)

    assert updated == _FULL_MESSAGE
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/samples/messages/1/updates/text"
    assert request.body == {}
    assert request.query["text"] == "новый текст"


async def test_update_message_last_write_time_query_and_empty_body(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "post",
        "/core/api/samples/messages/1/updates/lastWriteTime",
        body=_FULL_MESSAGE,
    )
    async with _Client(config=token_config) as ips:
        updated = await ips.update_message_last_write_time(1, "2026-06-25T12:00:00Z", confirm=True)

    assert updated == _FULL_MESSAGE
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/samples/messages/1/updates/lastWriteTime"
    assert request.body == {}
    assert request.query["lastWriteTime"] == "2026-06-25T12:00:00Z"
