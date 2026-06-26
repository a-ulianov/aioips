"""Тесты методов чтения раздела файлов."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_PROTOTYPE = {
    "prototypeId": 7001,
    "name": "Чертёж А4",
    "attributeId": 1042,
}

_BLOB_INFO = {
    "blobId": 778899,
    "realFileSize": 204800,
    "packedFileSize": 65536,
    "modifyDate": "2026-06-24T10:15:00Z",
    "fileName": "specification.pdf",
    "arcMethod": "zstd",
    "note": "Основной файл",
    "fileType": "ftNormal",
    "authorId": 500,
    "fileStorageId": 1029,
}

_FILE_ATTRIBUTE = {
    "attributeId": 1042,
    "attributeFieldType": "ftFile",
    "isMultiple": True,
    "fileInfoCollection": [_BLOB_INFO],
    "readOnly": False,
}

_OBJECT_WITH_FILES = {
    "objectVersionId": 102551,
    "objectType": 3,
    "readOnly": False,
    "attributes": [_FILE_ATTRIBUTE],
}


async def test_file_prototypes_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/files/getFilesProptotypes/102550",
        body=[_PROTOTYPE],
    )
    async with IPSClient(config=token_config) as ips:
        prototypes = await ips.file_prototypes(102550)

    assert len(prototypes) == 1
    proto = prototypes[0]
    assert proto.prototype_id == 7001
    assert proto.name == "Чертёж А4"
    assert proto.attribute_id == 1042


async def test_file_prototypes_attribute_id_optional(token_config: IPSConfig, fake_ips: FakeIPS):
    proto = {"prototypeId": 7002, "name": "Без атрибута"}
    fake_ips.add("get", "/core/api/files/getFilesProptotypes/102550", body=[proto])
    async with IPSClient(config=token_config) as ips:
        prototypes = await ips.file_prototypes(102550)

    assert prototypes[0].attribute_id is None


async def test_file_attributes_parses_nested(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/files/objects/102550", body=_OBJECT_WITH_FILES)
    async with IPSClient(config=token_config) as ips:
        obj = await ips.file_attributes(102550)

    assert obj.object_version_id == 102551
    assert obj.object_type == 3
    assert obj.read_only is False
    assert len(obj.attributes) == 1

    attr = obj.attributes[0]
    assert attr.attribute_id == 1042
    assert attr.attribute_field_type == "ftFile"
    assert attr.is_multiple is True
    assert len(attr.file_info_collection) == 1

    info = attr.file_info_collection[0]
    assert info.blob_id == 778899
    assert info.real_file_size == 204800
    assert info.packed_file_size == 65536
    assert info.file_name == "specification.pdf"
    assert info.arc_method == "zstd"
    assert info.file_type == "ftNormal"
    assert info.author_id == 500
    assert info.file_storage_id == 1029


async def test_file_attributes_coerces_null_lists(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {**_OBJECT_WITH_FILES, "attributes": None}
    fake_ips.add("get", "/core/api/files/objects/102550", body=body)
    async with IPSClient(config=token_config) as ips:
        obj = await ips.file_attributes(102550)

    assert obj.attributes == []


async def test_file_attributes_coerces_null_file_collection(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    attr = {**_FILE_ATTRIBUTE, "fileInfoCollection": None}
    body = {**_OBJECT_WITH_FILES, "attributes": [attr]}
    fake_ips.add("get", "/core/api/files/objects/102550", body=body)
    async with IPSClient(config=token_config) as ips:
        obj = await ips.file_attributes(102550)

    assert obj.attributes[0].file_info_collection == []


async def test_object_file_by_name_returns_string(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/files/objects/102550/files/byName/specification.pdf",
        body="file-content-bytes",
    )
    async with IPSClient(config=token_config) as ips:
        content = await ips.object_file_by_name(102550, "specification.pdf")

    assert content == "file-content-bytes"


async def test_object_file_by_name_encodes_special_chars(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    # Имя с пробелом/кириллицей URL-кодируется клиентом; сервер видит
    # декодированный путь, поэтому мок регистрируется по исходному имени.
    fake_ips.add(
        "get",
        "/core/api/files/objects/102550/files/byName/Чертёж А4.pdf",
        body="content",
    )
    async with IPSClient(config=token_config) as ips:
        content = await ips.object_file_by_name(102550, "Чертёж А4.pdf")

    assert content == "content"


async def test_object_file_by_blob_id_returns_string(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/files/objects/102550/files/778899",
        body="blob-content",
    )
    async with IPSClient(config=token_config) as ips:
        content = await ips.object_file_by_blob_id(102550, 778899)

    assert content == "blob-content"
