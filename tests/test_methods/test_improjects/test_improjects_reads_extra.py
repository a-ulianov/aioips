"""Тесты дополнительных read-методов раздела управления проектами (Improject)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_GRID_COLUMNS = {
    "columns": [
        {"id": "name", "width": 240},
        {"id": "progress"},
    ]
}


async def test_project_grid_columns_returns_columns(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/improjects/grid-columns", body=_GRID_COLUMNS)
    async with IPSClient(config=token_config) as ips:
        cols = await ips.grid_columns()

    assert len(cols.columns) == 2
    assert cols.columns[0] == {"id": "name", "width": 240}
    assert cols.columns[1]["id"] == "progress"


async def test_project_grid_columns_coerces_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/improjects/grid-columns", body={"columns": None})
    async with IPSClient(config=token_config) as ips:
        cols = await ips.grid_columns()

    assert cols.columns == []


async def test_task_attachments_allowed_types_returns_ints(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/improjects/tasks/attachments/allowed-types",
        body=[1037, 1041, 1052],
    )
    async with IPSClient(config=token_config) as ips:
        allowed = await ips.task_attachments_allowed_types()

    assert allowed == [1037, 1041, 1052]


async def test_task_attachments_allowed_types_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/improjects/tasks/attachments/allowed-types",
        body=[],
    )
    async with IPSClient(config=token_config) as ips:
        allowed = await ips.task_attachments_allowed_types()

    assert allowed == []
