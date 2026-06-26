"""Тесты мутаций файлов объекта (обратимый цикл add → delete и правки)."""

from datetime import UTC, datetime

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.files.update_object_file_info import UpdateObjectFileInfo

_Client = IPSClient

_BLOB_INFO: dict[str, object] = {
    "blobId": 778899,
    "realFileSize": 1024,
    "packedFileSize": 512,
    "modifyDate": "2026-06-25T10:00:00",
    "fileName": "schema.pdf",
    "arcMethod": "notPacked",
    "note": "",
    "fileType": "ftNormal",
    "authorId": 5,
    "fileStorageId": 7,
}


async def test_add_object_file_posts_multipart(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/files/objects/102550/files", body=_BLOB_INFO)
    async with _Client(config=token_config) as ips:
        info = await ips.add_object_file(
            object_id=102550,
            attribute_id=1031,
            file_data=b"%PDF-1.4 data",
            file_name="schema.pdf",
            file_type="ftNormal",
            modify_date_time=datetime(2026, 6, 25, 10, 0, tzinfo=UTC),
        )

    assert info.blob_id == 778899
    assert info.file_type == "ftNormal"
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/files/objects/102550/files"
    # multipart-тело не парсится как JSON фейковым сервером
    assert request.body is None


async def test_add_object_file_passes_real_file_size_query(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/files/objects/102550/files", body=_BLOB_INFO)
    async with _Client(config=token_config) as ips:
        await ips.add_object_file(
            object_id=102550,
            attribute_id=1031,
            file_data=b"x",
            file_name="x.bin",
            file_type="ftNormal",
            modify_date_time=datetime(2026, 6, 25, 10, 0, tzinfo=UTC),
            real_file_size=4096,
        )

    assert fake_ips.requests[-1].query == {"realFileSize": "4096"}


async def test_update_object_file_uses_put(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("put", "/core/api/files/objects/102550/files", body=_BLOB_INFO)
    async with _Client(config=token_config) as ips:
        info = await ips.update_object_file(
            object_id=102550,
            attribute_id=1031,
            blob_id=778899,
            file_data=b"%PDF-1.4 new",
            file_name="schema.pdf",
            modify_date_time=datetime(2026, 6, 25, 10, 0, tzinfo=UTC),
        )

    assert info.blob_id == 778899
    request = fake_ips.requests[-1]
    assert request.method == "PUT"
    assert request.path == "/core/api/files/objects/102550/files"


async def test_delete_object_file_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.delete_object_file(102550, attribute_id=1031, blob_id=778899)

    # запрос к серверу не делался
    assert fake_ips.requests == []


async def test_delete_object_file_passes_query(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("delete", "/core/api/files/objects/102550/files", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.delete_object_file(
            102550, attribute_id=1031, blob_id=778899, confirm=True
        )

    assert result is None
    request = fake_ips.requests[-1]
    assert request.method == "DELETE"
    assert request.path == "/core/api/files/objects/102550/files"
    assert request.query == {"attributeId": "1031", "blobId": "778899"}


async def test_update_object_file_info_sends_json(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("put", "/core/api/files/objects/102550/files/info", body=None)
    body = UpdateObjectFileInfo(
        attribute_id=1031,
        blob_id=778899,
        file_name="schema-rev2.pdf",
        note="Ревизия 2",
    )
    async with _Client(config=token_config) as ips:
        result = await ips.update_object_file_info(102550, body)

    assert result is None
    request = fake_ips.requests[-1]
    assert request.method == "PUT"
    assert request.path == "/core/api/files/objects/102550/files/info"
    assert request.body == {
        "blobId": 778899,
        "attributeId": 1031,
        "fileName": "schema-rev2.pdf",
        "note": "Ревизия 2",
    }


async def test_update_object_file_info_excludes_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("put", "/core/api/files/objects/102550/files/info", body=None)
    body = UpdateObjectFileInfo(attribute_id=1031, blob_id=778899)
    async with _Client(config=token_config) as ips:
        await ips.update_object_file_info(102550, body)

    # file_name и note (None) исключены из тела
    assert fake_ips.requests[-1].body == {"blobId": 778899, "attributeId": 1031}
