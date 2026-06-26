"""Тесты метода генерации содержимого табличного отчёта."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.table_report import ReportCreatorParams

CONTENT_URL = "/core/api/tableReport/102550/reportContent"


async def test_report_content_parses_and_builds_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        CONTENT_URL,
        body={
            "fileName": "report.frw",
            "objectId": 102550,
            "isTemplate": False,
            "isFormulaLib": False,
            "modified": False,
            "templateRoot": {"name": "root"},
            "docPages": [{"page": 1}],
            "formulas": None,
        },
    )
    async with IPSClient(config=token_config) as ips:
        content = await ips.report_content(
            102550,
            ReportCreatorParams(selected_ids=[5, 6], only_selected=True, parent_type_id=1742),
        )

    assert content.file_name == "report.frw"
    assert content.object_id == 102550
    assert content.doc_pages == [{"page": 1}]
    assert content.formulas == []  # null -> []

    request = next(r for r in fake_ips.requests if r.path == CONTENT_URL)
    assert request.method == "POST"
    assert request.body["selectedIds"] == [5, 6]
    assert request.body["onlySelected"] is True
    assert request.body["parentTypeId"] == 1742
