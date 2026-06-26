"""Тесты мутирующих методов загрузки/прикрепления файлов процесса (multipart)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient


async def test_create_attach_files_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.wf_create_attach_files(b"data", "a.pdf")

    assert fake_ips.requests == []


async def test_create_attach_files_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/wfAttachments/createAttachFiles", body=999001)
    async with _Client(config=token_config) as ips:
        obj_id = await ips.wf_create_attach_files(b"%PDF-1.4", "a.pdf", confirm=True)

    assert obj_id == 999001
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/wfAttachments/createAttachFiles"


async def test_create_attach_files_none_to_zero(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/wfAttachments/createAttachFiles", body=None)
    async with _Client(config=token_config) as ips:
        obj_id = await ips.wf_create_attach_files(b"x", "x", confirm=True)

    assert obj_id == 0


async def test_attach_files_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.wf_attach_files(48210, b"data", "a.pdf")

    assert fake_ips.requests == []


async def test_attach_files_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/wfAttachments/48210/attachFiles",
        body={"entity": {"objectId": 102550, "caption": "a.pdf"}, "isEntityPresent": True},
    )
    async with _Client(config=token_config) as ips:
        att = await ips.wf_attach_files(48210, b"%PDF-1.4", "a.pdf", confirm=True)

    assert att == {"objectId": 102550, "caption": "a.pdf"}
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/wfAttachments/48210/attachFiles"


async def test_attach_files_none_when_absent(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/wfAttachments/48210/attachFiles",
        body={"entity": None, "isEntityPresent": False},
    )
    async with _Client(config=token_config) as ips:
        att = await ips.wf_attach_files(48210, b"x", "x", confirm=True)

    assert att is None
