"""Тесты сервиса имён файлов и прикрепления временных файлов."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.files import AttachTempFile


async def test_file_unique_name_path_query_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/files/fileNamesService/getUniqueFileName",
        body="schema(1).pdf",
    )
    async with IPSClient(config=token_config) as ips:
        name = await ips.file_unique_name(file_name="schema.pdf", id=42)

    assert name == "schema(1).pdf"
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/files/fileNamesService/getUniqueFileName"
    assert request.method == "POST"
    assert request.body == {}
    assert request.query == {"fileName": "schema.pdf", "id": "42"}


async def test_file_unique_name_omits_unset_query(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/files/fileNamesService/getUniqueFileName", body="x.pdf")
    async with IPSClient(config=token_config) as ips:
        name = await ips.file_unique_name()

    assert name == "x.pdf"
    assert fake_ips.requests[-1].query == {}


async def test_next_file_id_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/files/fileNamesService/getNextFileID", body=4521)
    async with IPSClient(config=token_config) as ips:
        file_id = await ips.next_file_id()

    assert file_id == 4521
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/files/fileNamesService/getNextFileID"
    assert request.body == {}


async def test_file_id_by_name_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/files/fileNamesService/getIDByFileName", body=778899)
    async with IPSClient(config=token_config) as ips:
        file_id = await ips.file_id_by_name(file_name="schema.pdf")

    assert file_id == 778899
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/files/fileNamesService/getIDByFileName"
    assert request.body == {}
    assert request.query == {"fileName": "schema.pdf"}


async def test_file_id_by_name_none_to_zero(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/files/fileNamesService/getIDByFileName", body=None)
    async with IPSClient(config=token_config) as ips:
        file_id = await ips.file_id_by_name()

    assert file_id == 0


async def test_object_ids_by_file_name_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/files/fileNamesService/getObjectIDByFileName",
        body=[102550, 103001],
    )
    async with IPSClient(config=token_config) as ips:
        object_ids = await ips.object_ids_by_file_name(file_name="schema.pdf")

    assert object_ids == [102550, 103001]
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/files/fileNamesService/getObjectIDByFileName"
    assert request.body == {}
    assert request.query == {"fileName": "schema.pdf"}


async def test_object_ids_by_file_name_none_to_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/files/fileNamesService/getObjectIDByFileName",
        body=None,
    )
    async with IPSClient(config=token_config) as ips:
        object_ids = await ips.object_ids_by_file_name(file_name="missing.pdf")

    assert object_ids == []


async def test_attach_temp_files_body_and_path(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/files/objects/102550/attachTempFiles",
        body=[{"blobId": 778899}],
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.attach_temp_files(
            102550,
            [
                AttachTempFile(
                    attribute_id=12,
                    temp_file_name="temp_ab12.pdf",
                    file_type="ftNormal",
                    modify_date_time="2026-06-24T10:00:00",
                    real_file_size=1024,
                )
            ],
        )

    assert result == [{"blobId": 778899}]
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/files/objects/102550/attachTempFiles"
    assert request.method == "POST"
    assert isinstance(request.body, list)
    assert request.body[0]["attributeId"] == 12
    assert request.body[0]["tempFileName"] == "temp_ab12.pdf"
    assert request.body[0]["fileType"] == "ftNormal"
    assert request.body[0]["realFileSize"] == 1024


async def test_attach_temp_files_non_list_to_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/files/objects/1/attachTempFiles", body={"x": 1})
    async with IPSClient(config=token_config) as ips:
        result = await ips.attach_temp_files(1, [])

    assert result == []
