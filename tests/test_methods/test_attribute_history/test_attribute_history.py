"""Тесты методов раздела истории значений атрибутов."""

from datetime import datetime

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.attribute_history import AttributeHistoryRequest, HistoryType

_GET_PATH = "/core/api/attributeHistory/getHistory"
_DELETE_PATH = "/core/api/attributeHistory/deleteHistory"


def _request() -> AttributeHistoryRequest:
    return AttributeHistoryRequest(
        attribute_id=9,
        id=102550,
        type_id=1742,
        history_type=HistoryType.FOR_OBJECT,
    )


async def test_attribute_history_parses_records(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        _GET_PATH,
        body=[
            {"date": "2026-06-24T10:00:00Z", "value": "550.07.305", "user": "your-login"},
            {"date": None, "value": None, "user": None},
        ],
    )
    async with IPSClient(config=token_config) as ips:
        history = await ips.attribute_history(_request())

    assert len(history) == 2
    first = history[0]
    assert first.value == "550.07.305"
    assert first.user == "your-login"
    assert isinstance(first.date, datetime)
    assert history[1].date is None
    assert history[1].value is None

    req = next(r for r in fake_ips.requests if r.path == _GET_PATH)
    assert req.method == "POST"
    # тело сериализуется в camelCase
    assert req.body == {
        "attributeId": 9,
        "isRelation": False,
        "id": 102550,
        "typeId": 1742,
        "onlyPersonal": False,
        "historyType": "forObject",
    }


async def test_attribute_history_empty_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", _GET_PATH, body=[])
    async with IPSClient(config=token_config) as ips:
        history = await ips.attribute_history(_request())
    assert history == []


async def test_delete_attribute_history_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm"):
            await ips.delete_attribute_history(_request())
    # без confirm запрос НЕ должен уходить
    assert all(r.path != _DELETE_PATH for r in fake_ips.requests)


async def test_delete_attribute_history_with_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", _DELETE_PATH, status=204, body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.delete_attribute_history(
            AttributeHistoryRequest(
                attribute_id=9,
                type_id=1742,
                history_type=HistoryType.FOR_SAME_TYPE,
            ),
            confirm=True,
        )
    assert result is None

    req = next(r for r in fake_ips.requests if r.path == _DELETE_PATH)
    assert req.method == "POST"
    assert req.body["historyType"] == "forSameType"
    assert req.body["attributeId"] == 9
