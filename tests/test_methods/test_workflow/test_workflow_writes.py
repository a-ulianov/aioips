"""Тесты методов записи раздела процессов (workflow)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.workflow import Variable

_ATTACHMENT = {
    "objectId": 102550,
    "objectType": 1037,
    "caption": "Чертёж детали",
    "ownerId": 11,
    "objectTypeName": "Документ",
    "ownerName": "your-login",
    "checkOutBy": 0,
    "objectModifyMode": "checkout",
}


async def test_wf_save_variables_posts_body_array(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/wfVariables/48210/saveVariables", body=True)
    variables = [
        Variable(variable_name="Approved", variable_id=7, variable_type="boolean"),
    ]
    async with IPSClient(config=token_config) as ips:
        result = await ips.wf_save_variables(48210, variables)

    assert result is True
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/wfVariables/48210/saveVariables"
    # Тело — голый JSON-массив VariableDto (by_alias).
    assert req.body == [{"variableName": "Approved", "variableId": 7, "variableType": "boolean"}]


async def test_wf_add_attachments_posts_int_array(token_config: IPSConfig, fake_ips: FakeIPS):
    # Путь содержит опечатку IPS «addAttachmments» (двойная m).
    fake_ips.add(
        "post",
        "/core/api/wfAttachments/48210/addAttachmments",
        body={"attachments": [_ATTACHMENT], "hasInvisibleItems": False},
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.wf_add_attachments(48210, [102550])

    req = fake_ips.requests[-1]
    assert req.path == "/core/api/wfAttachments/48210/addAttachmments"
    assert req.body == [102550]
    assert len(result.attachments) == 1
    assert result.attachments[0].object_id == 102550
    assert result.has_invisible_items is False


async def test_wf_remove_attachments_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/wfAttachments/48210/removeAttachmments", body=None)
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.wf_remove_attachments(48210, [102550])

    # Без подтверждения запрос не уходит на сервер.
    assert fake_ips.requests == []


async def test_wf_remove_attachments_posts_int_array(token_config: IPSConfig, fake_ips: FakeIPS):
    # Путь содержит опечатку IPS «removeAttachmments» (двойная m).
    fake_ips.add("post", "/core/api/wfAttachments/48210/removeAttachmments", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.wf_remove_attachments(48210, [102550], confirm=True)

    assert result is None
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/wfAttachments/48210/removeAttachmments"
    assert req.body == [102550]


async def test_wf_attachments_data_posts_int_array(token_config: IPSConfig, fake_ips: FakeIPS):
    # Путь содержит опечатку IPS «getAttachmmentsData» (двойная m).
    fake_ips.add(
        "post",
        "/core/api/wfAttachments/getAttachmmentsData",
        body={"attachments": [_ATTACHMENT], "hasInvisibleItems": True},
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.wf_attachments_data([102550, 102551])

    req = fake_ips.requests[-1]
    assert req.path == "/core/api/wfAttachments/getAttachmmentsData"
    assert req.body == [102550, 102551]
    assert len(result.attachments) == 1
    assert result.attachments[0].object_id == 102550
    assert result.has_invisible_items is True
