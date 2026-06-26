"""Тесты методов чтения раздела редактора документов."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_NODE = {
    "lastChangeTimeTicks": 638000000000000000,
    "element": {"page": {"width": 210}},
    "childs": [
        {
            "lastChangeTimeTicks": 0,
            "element": {"table": {"rows": 2}},
            "childs": None,
            "isFirstCellInParentDataFlow": True,
            "isLastCellInParentDataFlow": False,
        }
    ],
    "isFirstCellInParentDataFlow": False,
    "isLastCellInParentDataFlow": True,
}


async def test_doc_editor_buffer_returns_tree(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/documentEditor/getBuffer", body=[_NODE])
    async with IPSClient(config=token_config) as ips:
        roots = await ips.doc_editor_buffer()

    assert len(roots) == 1
    root = roots[0]
    assert root.last_change_time_ticks == 638000000000000000
    assert root.element == {"page": {"width": 210}}
    assert root.is_last_cell_in_parent_data_flow is True
    assert len(root.childs) == 1
    # Дочерний childs=None должен превратиться в пустой список.
    assert root.childs[0]["childs"] is None


async def test_doc_editor_buffer_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/documentEditor/getBuffer", body=[])
    async with IPSClient(config=token_config) as ips:
        roots = await ips.doc_editor_buffer()

    assert roots == []


async def test_doc_editor_prop_name_passes_query(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/documentEditor/getPropName", body="Width")
    async with IPSClient(config=token_config) as ips:
        name = await ips.doc_editor_prop_name(props=3)

    assert name == "Width"
    assert fake_ips.requests[-1].query == {"props": "3"}


async def test_doc_editor_prop_name_none_query_and_empty(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/documentEditor/getPropName", body=None)
    async with IPSClient(config=token_config) as ips:
        name = await ips.doc_editor_prop_name()

    assert name == ""
    assert fake_ips.requests[-1].query == {}


async def test_doc_editor_non_assignable_prop_name(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/documentEditor/getNonAssignablePropName", body="Id")
    async with IPSClient(config=token_config) as ips:
        name = await ips.doc_editor_non_assignable_prop_name(props=7)

    assert name == "Id"
    assert fake_ips.requests[-1].query == {"props": "7"}


async def test_doc_editor_non_assignable_prop_name_empty(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/documentEditor/getNonAssignablePropName", body=None)
    async with IPSClient(config=token_config) as ips:
        name = await ips.doc_editor_non_assignable_prop_name()

    assert name == ""


async def test_doc_editor_all_fonts_name_update_query(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get", "/core/api/documentEditor/getAllFontsName", body=["Arial", "Times New Roman"]
    )
    async with IPSClient(config=token_config) as ips:
        fonts = await ips.doc_editor_all_fonts_name(update=True)

    assert fonts == ["Arial", "Times New Roman"]
    assert fake_ips.requests[-1].query == {"update": "true"}


async def test_doc_editor_all_fonts_name_no_query(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/documentEditor/getAllFontsName", body=[])
    async with IPSClient(config=token_config) as ips:
        fonts = await ips.doc_editor_all_fonts_name()

    assert fonts == []
    assert fake_ips.requests[-1].query == {}


async def test_doc_editor_font_list_true(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/documentEditor/font/getFontList", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.doc_editor_font_list()

    assert result is True


async def test_doc_editor_font_list_null_is_false(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/documentEditor/font/getFontList", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.doc_editor_font_list()

    assert result is False
