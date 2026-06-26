"""Тесты методов чтения раздела документов.

Раздел ``documents`` пока не подключён к публичному ``IPSClient``, поэтому
методы вызываются через агрегатор раздела :class:`DocumentsAPI`, который сам
наследует ядро клиента и работает как асинхронный контекстный менеджер.
"""

from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.methods.documents import DocumentsAPI

_PROTOTYPE = {
    "prototypeId": 7,
    "prototypeName": "Чертёж А4",
    "prototypeFilePatternName": "draw_*.cdw",
    "prototypeFileName": "draw_a4.cdw",
}

_SETTINGS = {
    "documentFileExtension": "pdf",
    "additionalDocumentFileExtension": "tif",
    "documentTypeName": "Чертёж",
    "documentTypeCode": "ЧТ",
    "isShowDocumentNameInStamp": True,
    "isDocumentTypeIncludeCodeInDesignation": False,
    "outputObjectTypeIds": [101, 102],
    "subscribers": [
        {"subscriberId": 3, "subscriberName": "Архив", "copiesCount": 2},
    ],
    "filePrototypeIds": [7, 8],
}


async def test_document_prototypes_common_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/api/documents/prototypes/common", body=[_PROTOTYPE, _PROTOTYPE])
    async with DocumentsAPI(config=token_config) as ips:
        prototypes = await ips.document_prototypes_common()

    assert len(prototypes) == 2
    proto = prototypes[0]
    assert proto.prototype_id == 7
    assert proto.prototype_name == "Чертёж А4"
    assert proto.prototype_file_pattern_name == "draw_*.cdw"
    assert proto.prototype_file_name == "draw_a4.cdw"


async def test_document_prototypes_private_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/api/documents/prototypes/private", body=[_PROTOTYPE])
    async with DocumentsAPI(config=token_config) as ips:
        prototypes = await ips.document_prototypes_private()

    assert len(prototypes) == 1
    assert prototypes[0].prototype_id == 7
    assert prototypes[0].prototype_file_name == "draw_a4.cdw"


async def test_document_settings_returns_object(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/api/documents/1024/settings", body=_SETTINGS)
    async with DocumentsAPI(config=token_config) as ips:
        settings = await ips.document_settings(1024)

    assert settings.document_file_extension == "pdf"
    assert settings.additional_document_file_extension == "tif"
    assert settings.document_type_name == "Чертёж"
    assert settings.document_type_code == "ЧТ"
    assert settings.is_show_document_name_in_stamp is True
    assert settings.is_document_type_include_code_in_designation is False
    assert settings.output_object_type_ids == [101, 102]
    assert settings.file_prototype_ids == [7, 8]
    assert len(settings.subscribers) == 1
    assert settings.subscribers[0].subscriber_id == 3
    assert settings.subscribers[0].subscriber_name == "Архив"
    assert settings.subscribers[0].copies_count == 2

    captured = fake_ips.requests[-1]
    assert captured.path == "/api/documents/1024/settings"


async def test_document_settings_coerces_null_lists(token_config: IPSConfig, fake_ips: FakeIPS):
    settings_body = {
        **_SETTINGS,
        "outputObjectTypeIds": None,
        "subscribers": None,
        "filePrototypeIds": None,
    }
    fake_ips.add("get", "/api/documents/1024/settings", body=settings_body)
    async with DocumentsAPI(config=token_config) as ips:
        settings = await ips.document_settings(1024)

    assert settings.output_object_type_ids == []
    assert settings.subscribers == []
    assert settings.file_prototype_ids == []
