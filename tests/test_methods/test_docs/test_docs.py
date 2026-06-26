"""Тесты раздела docs (типы и настройки документов) IPS Web API.

Категория A — чтения через POST (без confirm): проверяем путь, тело/query и
распаковку результата. Категория B — мутация ``set_doc_settings``: гейт
``confirm`` (без него — ``ValueError`` до запроса) и корректный путь/тело при
``confirm=True``.
"""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.client import IPSClient

_Client = IPSClient

_SETTINGS = {"documentType": 1742, "fileExtensions": [".pdf", ".dwg"]}


# ---------------------------------------------------------------------------
# Категория A: чтения через POST (без confirm)
# ---------------------------------------------------------------------------


async def test_doc_suffixes(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/docs/GetDocSuffixes", body=["-01", "-02"])
    async with _Client(config=token_config) as ips:
        result = await ips.doc_suffixes()

    assert result == ["-01", "-02"]
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/docs/GetDocSuffixes"
    assert request.body == {}


async def test_doc_suffixes_null_to_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/docs/GetDocSuffixes", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.doc_suffixes()

    assert result == []


async def test_document_types_by_file_ext(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/docs/GetDocumentTypesByFileExt", body=[1742, 1801])
    async with _Client(config=token_config) as ips:
        result = await ips.document_types_by_file_ext(".pdf")

    assert result == [1742, 1801]
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.body == {}
    assert request.query == {"fileExt": ".pdf"}


async def test_document_types_by_file_ext_no_param(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/docs/GetDocumentTypesByFileExt", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.document_types_by_file_ext()

    assert result == []
    assert fake_ips.requests[-1].query == {}


async def test_document_types_by_output_object_types(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/docs/GetDocumentTypesByOutputObjectTypes", body=[1742])
    async with _Client(config=token_config) as ips:
        result = await ips.document_types_by_output_object_types(
            [1024, 1042], root_document_object_type=1001
        )

    assert result == [1742]
    request = fake_ips.requests[-1]
    assert request.body == [1024, 1042]
    assert request.query == {"rootDocumentObjectType": "1001"}


async def test_document_types_by_output_object_types_no_root(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/docs/GetDocumentTypesByOutputObjectTypes", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.document_types_by_output_object_types([1024])

    assert result == []
    request = fake_ips.requests[-1]
    assert request.body == [1024]
    assert request.query == {}


async def test_doc_settings(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/docs/GetSettings", body=_SETTINGS)
    async with _Client(config=token_config) as ips:
        result = await ips.doc_settings(document_type=1742)

    assert result == _SETTINGS
    request = fake_ips.requests[-1]
    assert request.body == {}
    assert request.query == {"documentType": "1742"}


async def test_doc_settings_null_to_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/docs/GetSettings", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.doc_settings()

    assert result == {}
    assert fake_ips.requests[-1].query == {}


async def test_doc_settings_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/docs/GetSettingsList", body=[_SETTINGS, {"documentType": 1801}])
    async with _Client(config=token_config) as ips:
        result = await ips.doc_settings_list([1742, 1801])

    assert result == [_SETTINGS, {"documentType": 1801}]
    assert fake_ips.requests[-1].body == [1742, 1801]


async def test_doc_settings_list_null_to_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/docs/GetSettingsList", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.doc_settings_list([1742])

    assert result == []


async def test_inherited_from_constructor_documents(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/docs/InheritedFromConstructorDocuments", body=True)
    async with _Client(config=token_config) as ips:
        result = await ips.inherited_from_constructor_documents(1742)

    assert result is True
    request = fake_ips.requests[-1]
    assert request.body == {}
    assert request.query == {"documentType": "1742"}


async def test_inherited_from_documents(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/docs/InheritedFromDocuments", body=False)
    async with _Client(config=token_config) as ips:
        result = await ips.inherited_from_documents(1742)

    assert result is False
    request = fake_ips.requests[-1]
    assert request.body == {}
    assert request.query == {"documentType": "1742"}


# ---------------------------------------------------------------------------
# Категория B: мутация — гейт confirm и корректный вызов
# ---------------------------------------------------------------------------


async def test_set_doc_settings_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.set_doc_settings(_SETTINGS, document_type=1742)

    assert fake_ips.requests == []


async def test_set_doc_settings_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/docs/SetSettings", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.set_doc_settings(_SETTINGS, document_type=1742, confirm=True)

    assert result is None
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/docs/SetSettings"
    assert request.body == _SETTINGS
    assert request.query == {"documentType": "1742"}
