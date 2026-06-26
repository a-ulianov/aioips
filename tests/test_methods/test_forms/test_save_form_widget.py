"""Тесты метода ``save_form_widget`` (сохранение виджета формы, мутация)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.client import IPSClient

_Client = IPSClient

_WIDGET = {"id": "w1", "name": "root", "widgetType": "form", "widgets": []}


async def test_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.save_form_widget(_WIDGET, form_id=540)
    assert fake_ips.requests == []


async def test_confirm_true_posts_body_and_query(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/forms/saveFormWidget", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.save_form_widget(_WIDGET, form_id=540, confirm=True)
    assert result is None
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/core/api/forms/saveFormWidget"
    assert req.body == _WIDGET
    assert req.query["formId"] == "540"


async def test_form_id_omitted_when_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/forms/saveFormWidget", body=None)
    async with _Client(config=token_config) as ips:
        await ips.save_form_widget(_WIDGET, confirm=True)
    req = fake_ips.requests[-1]
    assert "formId" not in req.query
