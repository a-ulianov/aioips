"""Тесты дополнительных методов редактора документов (чтения через POST и мутации сессии).

Покрывает:
- чтения через POST (без confirm): свойства элемента, дочерние узлы страницы, SVG
  страницы, представление общих формул, предпросмотр текста;
- мутации сессии (с confirm-гейтом): сохранение шрифта, пакет транзакций правок,
  закрытие/удаление/сохранение открытого документа.
"""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient

_GUID = "11111111-1111-1111-1111-111111111111"
_BLOB = 42


# --- A. Чтения через POST (без confirm) -------------------------------------------


async def test_element_props_returns_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/documentEditor/content/getElementProps", body={"width": 210})
    async with _Client(config=token_config) as ips:
        props = await ips.doc_editor_element_props({"pageId": 1, "elementId": 7})

    assert props == {"width": 210}
    assert fake_ips.requests[-1].method == "POST"
    assert fake_ips.requests[-1].body == {"pageId": 1, "elementId": 7}


async def test_element_props_none_body_is_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/documentEditor/content/getElementProps", body=None)
    async with _Client(config=token_config) as ips:
        props = await ips.doc_editor_element_props()

    assert props == {}
    assert fake_ips.requests[-1].body == {}


async def test_page_child_nodes_returns_model(token_config: IPSConfig, fake_ips: FakeIPS):
    payload = {"page": {"id": 1}, "dpi": 96, "pagesOrderId": 5, "pageNames": ["p1"]}
    fake_ips.add("post", "/core/api/documentEditor/content/pageChildNodes", body=payload)
    async with _Client(config=token_config) as ips:
        content = await ips.doc_editor_page_child_nodes({"pageId": 1})

    assert content["dpi"] == 96
    assert content["pageNames"] == ["p1"]
    assert fake_ips.requests[-1].body == {"pageId": 1}


async def test_page_svg_returns_model(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post", "/core/api/documentEditor/content/pageSvg", body={"page": {"svg": "<svg/>"}}
    )
    async with _Client(config=token_config) as ips:
        svg_model = await ips.doc_editor_page_svg({"pageId": 1})

    assert svg_model["page"] == {"svg": "<svg/>"}
    assert fake_ips.requests[-1].path == "/core/api/documentEditor/content/pageSvg"


async def test_general_formulas_view_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    body = [{"id": 1, "svgImage": "<svg/>", "formulaText": "a+b"}]
    fake_ips.add("post", "/core/api/documentEditor/formulas/getGeneralFormulasView", body=body)
    async with _Client(config=token_config) as ips:
        views = await ips.doc_editor_general_formulas_view([{"id": 1, "formulaText": "a+b"}])

    assert views == body
    assert fake_ips.requests[-1].body == [{"id": 1, "formulaText": "a+b"}]


async def test_general_formulas_view_none_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/documentEditor/formulas/getGeneralFormulasView", body=None)
    async with _Client(config=token_config) as ips:
        views = await ips.doc_editor_general_formulas_view()

    assert views == []
    assert fake_ips.requests[-1].body == []


async def test_text_modal_setting_preview_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/documentEditor/preview", body="Узел 1")
    async with _Client(config=token_config) as ips:
        text = await ips.doc_editor_text_modal_setting_preview({"template": "{n}"})

    assert text == "Узел 1"
    assert fake_ips.requests[-1].body == {"template": "{n}"}


async def test_text_modal_setting_preview_none_is_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/documentEditor/preview", body=None)
    async with _Client(config=token_config) as ips:
        text = await ips.doc_editor_text_modal_setting_preview()

    assert text == ""


# --- B. Мутации сессии (confirm-гейт) ---------------------------------------------


async def test_save_font_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.doc_editor_save_font({"name": "MyFont"})
    # Запрос не должен был уйти на сервер.
    assert fake_ips.requests == []


async def test_save_font_confirm_true(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/documentEditor/font/saveFont", body=True)
    async with _Client(config=token_config) as ips:
        ok = await ips.doc_editor_save_font({"name": "MyFont"}, confirm=True)

    assert ok is True
    assert fake_ips.requests[-1].body == {"name": "MyFont"}


async def test_execute_batch_transactions_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.doc_editor_execute_batch_transactions({"transactions": []})
    assert fake_ips.requests == []


async def test_execute_batch_transactions_confirm_true(token_config: IPSConfig, fake_ips: FakeIPS):
    result_body = {
        "changedPagesIds": [1, 2],
        "createdElementIds": [10],
        "pageOrderChanged": False,
    }
    fake_ips.add("post", "/core/api/documentEditor/execute/batch/transactions", body=result_body)
    async with _Client(config=token_config) as ips:
        result = await ips.doc_editor_execute_batch_transactions(
            {"transactions": [{"op": "add"}]}, confirm=True
        )

    assert result == result_body
    assert fake_ips.requests[-1].body == {"transactions": [{"op": "add"}]}


async def test_close_document_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.doc_editor_close_document(_GUID, _BLOB)
    assert fake_ips.requests == []


async def test_close_document_confirm_true(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/documentEditor/openDocument/{_GUID}/{_BLOB}/close"
    fake_ips.add("post", path, body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.doc_editor_close_document(_GUID, _BLOB, mode="view", confirm=True)

    assert result is None
    req = fake_ips.requests[-1]
    assert req.path == path
    assert req.body == {}
    assert req.query == {"mode": "view"}


async def test_remove_from_open_documents_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.doc_editor_remove_from_open_documents(_GUID, _BLOB)
    assert fake_ips.requests == []


async def test_remove_from_open_documents_confirm_true(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/documentEditor/openDocument/{_GUID}/{_BLOB}/remove"
    fake_ips.add("delete", path, body=True)
    async with _Client(config=token_config) as ips:
        ok = await ips.doc_editor_remove_from_open_documents(_GUID, _BLOB, confirm=True)

    assert ok is True
    assert fake_ips.requests[-1].method == "DELETE"
    assert fake_ips.requests[-1].path == path


async def test_save_document_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.doc_editor_save_document(_GUID, _BLOB)
    assert fake_ips.requests == []


async def test_save_document_confirm_true_with_query(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/documentEditor/openDocument/{_GUID}/{_BLOB}/save"
    body = {"modified": True, "objectId": 777, "fileBlobId": _BLOB}
    fake_ips.add("post", path, body=body)
    async with _Client(config=token_config) as ips:
        result = await ips.doc_editor_save_document(
            _GUID,
            _BLOB,
            is_virtual_document=True,
            type_id=1742,
            confirm=True,
        )

    assert result == body
    req = fake_ips.requests[-1]
    assert req.body == {}
    assert req.query == {"isVirtualDocument": "true", "typeId": "1742"}
