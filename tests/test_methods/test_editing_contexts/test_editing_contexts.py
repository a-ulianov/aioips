"""Тесты методов раздела контекстов редактирования."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.editing_contexts import (
    AddObjectsToContext,
    AddObjectsToEditingContextType,
    ReplaceVersionInEditingContext,
    UpdateEditingContextObjectsIn,
)

_Client = IPSClient


async def test_add_objects_to_editing_context_sends_body_and_unwraps(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "post",
        "/core/api/editingContexts/501/add",
        body={
            "result": {
                "editingContextLogEntities": [
                    {"errorCode": "none", "errorDescription": None, "objectVersionId": 102551}
                ],
                "addedObjectsCount": 1,
                "skippedObjectsCount": 1,
            },
            "modificationsHistory": [],
        },
    )
    body = AddObjectsToContext(
        object_version_ids=[102550, 102551],
        add_objects_to_context_type=AddObjectsToEditingContextType.OBJECTS_WITH_COMPOSITION,
    )
    async with _Client(config=token_config) as ips:
        result = await ips.add_objects_to_editing_context(501, body)

    assert result.added_objects_count == 1
    assert result.skipped_objects_count == 1
    assert len(result.editing_context_log_entities) == 1

    sent = fake_ips.requests[-1]
    assert sent.method == "POST"
    assert sent.path == "/core/api/editingContexts/501/add"
    assert sent.body == {
        "objectVersionIds": [102550, 102551],
        "addObjectsToContextType": "objectsWithComposition",
    }


async def test_add_objects_to_editing_context_validates_raw_dto(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "post",
        "/core/api/editingContexts/7/add",
        body={
            "editingContextLogEntities": None,
            "addedObjectsCount": 3,
            "skippedObjectsCount": 0,
        },
    )
    body = AddObjectsToContext(
        object_version_ids=[1, 2, 3],
        add_objects_to_context_type=AddObjectsToEditingContextType.OBJECTS,
    )
    async with _Client(config=token_config) as ips:
        result = await ips.add_objects_to_editing_context(7, body)

    assert result.added_objects_count == 3
    assert result.editing_context_log_entities == []


async def test_replace_version_in_editing_context_sends_body(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/editingContexts/501/replace", body=None)
    body = ReplaceVersionInEditingContext(
        editing_context_version_id=102550,
        replacement_version_id=102560,
    )
    async with _Client(config=token_config) as ips:
        result = await ips.replace_version_in_editing_context(501, body)

    assert result is None
    sent = fake_ips.requests[-1]
    assert sent.method == "POST"
    assert sent.path == "/core/api/editingContexts/501/replace"
    assert sent.body == {
        "editingContextVersionId": 102550,
        "replacementVersionId": 102560,
    }


async def test_update_editing_context_objects_sends_body(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/editingContexts/501/update", body=None)
    body = UpdateEditingContextObjectsIn(object_version_ids=[102550, 102551])
    async with _Client(config=token_config) as ips:
        result = await ips.update_editing_context_objects(501, body)

    assert result is None
    sent = fake_ips.requests[-1]
    assert sent.method == "POST"
    assert sent.path == "/core/api/editingContexts/501/update"
    assert sent.body == {"objectVersionIds": [102550, 102551]}
