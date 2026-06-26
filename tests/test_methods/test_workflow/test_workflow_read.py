"""Тесты методов чтения раздела процессов (workflow)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.common.enumerations import ObjectModifyMode

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

_VARIABLE = {
    "variableName": "Approved",
    "variableId": 7,
    "variableType": "boolean",
    "shortName": "Утверждено",
}


async def test_wf_attachments_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/wfAttachments/48210/getAttachmments",
        body={"attachments": [_ATTACHMENT], "hasInvisibleItems": True},
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.wf_attachments(48210)

    assert result.has_invisible_items is True
    assert len(result.attachments) == 1
    att = result.attachments[0]
    assert att.object_id == 102550
    assert att.object_type == 1037
    assert att.caption == "Чертёж детали"
    assert att.owner_id == 11
    assert att.object_type_name == "Документ"
    assert att.owner_name == "your-login"
    assert att.check_out_by == 0
    assert att.object_modify_mode is ObjectModifyMode.CHECKOUT


async def test_wf_attachments_coerces_null_attachments(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/wfAttachments/48210/getAttachmments",
        body={"attachments": None, "hasInvisibleItems": False},
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.wf_attachments(48210)

    assert result.attachments == []
    assert result.has_invisible_items is False


async def test_wf_attachment_allowed_types_returns_ints(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/wfAttachments/48210/allowedtypes", body=[1037, 1040])
    async with IPSClient(config=token_config) as ips:
        result = await ips.wf_attachment_allowed_types(48210)

    assert result == [1037, 1040]


async def test_wf_variables_returns_list_without_filter(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/wfVariables/48210/loadVariables",
        body=[_VARIABLE],
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.wf_variables(48210)

    assert len(result) == 1
    var = result[0]
    assert var.variable_name == "Approved"
    assert var.variable_id == 7
    assert var.variable_type == "boolean"
    assert var.short_name == "Утверждено"
    # Без фильтра query-параметр не отправляется.
    assert fake_ips.requests[-1].query == {}


async def test_wf_variables_sends_global_filter(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/wfVariables/48210/loadVariables", body=[_VARIABLE])
    async with IPSClient(config=token_config) as ips:
        await ips.wf_variables(48210, is_global_variable=True)

    assert fake_ips.requests[-1].query == {"isGlobalVariable": "true"}
