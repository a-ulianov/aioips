"""Тесты методов чтения содержимого/шрифта/формул редактора документов.

Проверяют путь, query (``mode``) и распаковку ответа против поддельного
сервера :class:`FakeIPS`.
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient
_GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"


async def test_doc_editor_content_path_and_mode(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/documentEditor/{_GUID}/content/42"
    fake_ips.add("get", path, body={"pages": 3})
    async with _Client(config=token_config) as ips:
        content = await ips.doc_editor_content(_GUID, 42, mode="view")

    assert content == {"pages": 3}
    request = fake_ips.requests[-1]
    assert request.path == path
    assert request.query == {"mode": "view"}


async def test_doc_editor_content_omits_mode(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/documentEditor/{_GUID}/content/7"
    fake_ips.add("get", path, body={})
    async with _Client(config=token_config) as ips:
        assert await ips.doc_editor_content(_GUID, 7) == {}

    assert fake_ips.requests[-1].query == {}


async def test_doc_editor_complect_content(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/documentEditor/{_GUID}/complectDocumentContent"
    fake_ips.add("get", path, body={"complect": True})
    async with _Client(config=token_config) as ips:
        content = await ips.doc_editor_complect_document_content(_GUID)

    assert content == {"complect": True}
    assert fake_ips.requests[-1].path == path


async def test_doc_editor_complect_content_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/documentEditor/{_GUID}/complectDocumentContent"
    fake_ips.add("get", path, body=None)
    async with _Client(config=token_config) as ips:
        assert await ips.doc_editor_complect_document_content(_GUID) == {}


async def test_doc_editor_get_font(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/documentEditor/font/getFont"
    fake_ips.add("get", path, body={"name": "Arial"})
    async with _Client(config=token_config) as ips:
        font = await ips.doc_editor_get_font()

    assert font == {"name": "Arial"}
    assert fake_ips.requests[-1].path == path
    assert fake_ips.requests[-1].query == {}


async def test_doc_editor_get_font_scalar_to_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    # Swagger объявляет ответ boolean: скалярный ответ распаковывается в {}.
    path = "/core/api/documentEditor/font/getFont"
    fake_ips.add("get", path, body=True)
    async with _Client(config=token_config) as ips:
        assert await ips.doc_editor_get_font() == {}


async def test_doc_editor_formulas_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/documentEditor/{_GUID}/formulas/42"
    fake_ips.add("get", path, body=[{"name": "A1"}, {"name": "B2"}])
    async with _Client(config=token_config) as ips:
        formulas = await ips.doc_editor_formulas(_GUID, 42, mode="view")

    assert formulas == [{"name": "A1"}, {"name": "B2"}]
    request = fake_ips.requests[-1]
    assert request.path == path
    assert request.query == {"mode": "view"}


async def test_doc_editor_formulas_empty_on_null(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/documentEditor/{_GUID}/formulas/1"
    fake_ips.add("get", path, body=None)
    async with _Client(config=token_config) as ips:
        assert await ips.doc_editor_formulas(_GUID, 1) == []

    assert fake_ips.requests[-1].query == {}
