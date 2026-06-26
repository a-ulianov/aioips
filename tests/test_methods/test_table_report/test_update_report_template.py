"""Тесты метода ``update_report_template`` (сохранение шаблона табличного отчёта)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.client import IPSClient

_Client = IPSClient

_TEMPLATE = {"templateID": 7, "reportID": 3, "columns": []}


async def test_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.update_report_template(_TEMPLATE)
    assert fake_ips.requests == []


async def test_confirm_true_posts_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/tableReport/create", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.update_report_template(_TEMPLATE, confirm=True)
    assert result is None
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/core/api/tableReport/create"
    assert req.body == _TEMPLATE
