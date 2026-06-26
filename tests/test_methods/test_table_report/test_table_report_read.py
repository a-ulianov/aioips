"""Тесты методов чтения раздела табличных отчётов.

Раздел ``table_report`` пока не подключён к :class:`IPSClient`, поэтому тесты
используют его агрегатор :class:`TableReportAPI` как самостоятельный клиент
(он наследует ядро ``APIManager`` и работает как асинхронный контекстный менеджер).
"""

from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.methods.table_report import TableReportAPI

_REPORT = {
    "templateID": 7,
    "templateName": "Спецификация",
    "reportID": 42,
    "reportName": "BOM",
    "reportCaption": "Ведомость",
    "columns": [{"id": 1, "caption": "Поз."}, {"id": 2, "caption": "Кол-во"}],
    "rowNumbers": True,
    "rowNumbersColumnWidth": 8,
    "rowNumbersColumnCaption": "№",
    "resultItem": True,
    "countItems": False,
    "datePrint": "date",
    "pageNumber": "downCenter",
    "generatedDocTypeGuid": "cad001c5-306c-11d8-b4e9-00304f19f545",
}


async def test_table_report_parses_acronym_ids(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/tableReport/102550/get", body=_REPORT)
    async with TableReportAPI(config=token_config) as ips:
        report = await ips.table_report(102550)

    # Акроним-алиасы templateID/reportID должны корректно сопоставиться.
    assert report.template_id == 7
    assert report.report_id == 42
    assert report.template_name == "Спецификация"
    assert report.report_caption == "Ведомость"
    assert len(report.columns) == 2
    assert report.row_numbers is True
    assert report.row_numbers_column_width == 8
    assert report.result_item is True
    assert report.count_items is False
    assert report.date_print == "date"
    assert report.page_number == "downCenter"
    assert report.generated_doc_type_guid == "cad001c5-306c-11d8-b4e9-00304f19f545"


async def test_table_report_math_total_sends_query(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/tableReport/getMathTotal", body="120.5")
    async with TableReportAPI(config=token_config) as ips:
        total = await ips.table_report_math_total(math_total="sum(weight)")

    assert total == "120.5"
    captured = fake_ips.requests[-1]
    assert captured.query.get("mathTotal") == "sum(weight)"


async def test_table_report_math_total_none_returns_empty(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with TableReportAPI(config=token_config) as ips:
        total = await ips.table_report_math_total()

    # При math_total=None запрос не отправляется и возвращается пустая строка.
    assert total == ""
    assert fake_ips.requests == []
