"""Тесты методов записи/мутаций раздела управления проектами (Improject).

Для каждого метода проверяем: гейт ``confirm`` (без него — ``ValueError`` до
запроса) и при ``confirm=True`` — корректный HTTP-метод, путь, query/тело и
распаковку результата (для ``*ProcessResultWithLogInfoDto`` — ключ ``result``).
"""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.client import IPSClient
from aioips.schemas.improjects import ScaleType

_Client = IPSClient

_GANTT = {"action": {"type": "update", "id": 7200}}
_CREATE_PROJECT = {"objectId": 102600}
_CREATE_TASK = {"tid": 7201, "action": {"type": "add"}}
_TASK_INFO_WRAP = {
    "result": {"projectId": 1500, "taskData": {"id": 7200, "progress": 0.5}},
    "modificationsHistory": [],
}
_STATUS_WRAP = {"result": {"status": "executing"}, "modificationsHistory": None}


# ---------------------------------------------------------------------------
# create_project
# ---------------------------------------------------------------------------


async def test_create_project_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.create_project({"name": "X"})

    assert fake_ips.requests == []


async def test_create_project_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/improjects/project", body=_CREATE_PROJECT)
    async with _Client(config=token_config) as ips:
        res = await ips.create_project({"objectTypeId": 4, "name": "X"}, confirm=True)

    assert res["objectId"] == 102600
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.body == {"objectTypeId": 4, "name": "X"}


# ---------------------------------------------------------------------------
# create_task
# ---------------------------------------------------------------------------


async def test_create_task_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.create_task(1500, {"taskData": {"text": "T"}})

    assert fake_ips.requests == []


async def test_create_task_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/improjects/1500/task", body=_CREATE_TASK)
    async with _Client(config=token_config) as ips:
        res = await ips.create_task(1500, {"taskData": {"text": "T"}}, confirm=True)

    assert res["tid"] == 7201
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.body == {"taskData": {"text": "T"}}


# ---------------------------------------------------------------------------
# create_dependency
# ---------------------------------------------------------------------------


async def test_create_dependency_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.create_dependency(1500, {"source": 1, "target": 2})

    assert fake_ips.requests == []


async def test_create_dependency_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/improjects/1500/dependency", body=_CREATE_TASK)
    async with _Client(config=token_config) as ips:
        res = await ips.create_dependency(1500, {"source": 1, "target": 2}, confirm=True)

    assert res["tid"] == 7201
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.body == {"source": 1, "target": 2}


# ---------------------------------------------------------------------------
# update_task
# ---------------------------------------------------------------------------


async def test_update_task_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.update_task(7200, {"taskData": {"id": 7200}})

    assert fake_ips.requests == []


async def test_update_task_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("put", "/core/api/improjects/task/7200", body=_GANTT)
    async with _Client(config=token_config) as ips:
        res = await ips.update_task(7200, {"taskData": {"id": 7200}}, confirm=True)

    assert res["action"]["type"] == "update"
    request = fake_ips.requests[-1]
    assert request.method == "PUT"
    assert request.body == {"taskData": {"id": 7200}}


# ---------------------------------------------------------------------------
# delete_task
# ---------------------------------------------------------------------------


async def test_delete_task_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.delete_task(7200)

    assert fake_ips.requests == []


async def test_delete_task_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("delete", "/core/api/improjects/task/7200", body=_GANTT)
    async with _Client(config=token_config) as ips:
        res = await ips.delete_task(7200, confirm=True)

    assert res["action"]["id"] == 7200
    assert fake_ips.requests[-1].method == "DELETE"


# ---------------------------------------------------------------------------
# update_dependency / delete_dependency
# ---------------------------------------------------------------------------


async def test_update_dependency_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.update_dependency(10, {"source": 1, "target": 3})

    assert fake_ips.requests == []


async def test_update_dependency_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("put", "/core/api/improjects/dependency/10", body=_GANTT)
    async with _Client(config=token_config) as ips:
        res = await ips.update_dependency(10, {"source": 1, "target": 3}, confirm=True)

    assert res["action"]["type"] == "update"
    request = fake_ips.requests[-1]
    assert request.method == "PUT"
    assert request.body == {"source": 1, "target": 3}


async def test_delete_dependency_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.delete_dependency(10)

    assert fake_ips.requests == []


async def test_delete_dependency_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("delete", "/core/api/improjects/dependency/10", body=_GANTT)
    async with _Client(config=token_config) as ips:
        res = await ips.delete_dependency(10, confirm=True)

    assert res["action"]["type"] == "update"
    assert fake_ips.requests[-1].method == "DELETE"


# ---------------------------------------------------------------------------
# move_task_level_down / move_task_level_up / reorder_task
# ---------------------------------------------------------------------------


async def test_move_task_level_down_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.move_task_level_down(7200)

    assert fake_ips.requests == []


async def test_move_task_level_down_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/improjects/task/7200/moveLevelDown", body=_GANTT)
    async with _Client(config=token_config) as ips:
        res = await ips.move_task_level_down(7200, new_parent_task_id=7100, confirm=True)

    assert res["action"]["type"] == "update"
    request = fake_ips.requests[-1]
    assert request.query["newParentTaskId"] == "7100"
    assert request.body == {}


async def test_move_task_level_up_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.move_task_level_up(7200)

    assert fake_ips.requests == []


async def test_move_task_level_up_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/improjects/task/7200/moveLevelUp", body=_GANTT)
    async with _Client(config=token_config) as ips:
        res = await ips.move_task_level_up(7200, new_prev_task_id=7050, confirm=True)

    assert res["action"]["type"] == "update"
    request = fake_ips.requests[-1]
    assert request.query["newPrevTaskId"] == "7050"
    assert "newParentTaskId" not in request.query
    assert request.body == {}


async def test_reorder_task_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.reorder_task(7200)

    assert fake_ips.requests == []


async def test_reorder_task_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/improjects/task/7200/reorder", body=_GANTT)
    async with _Client(config=token_config) as ips:
        res = await ips.reorder_task(
            7200,
            new_parent_task_id=7100,
            new_prev_task_id=7050,
            new_next_task_id=7300,
            confirm=True,
        )

    assert res["action"]["type"] == "update"
    request = fake_ips.requests[-1]
    assert request.query["newParentTaskId"] == "7100"
    assert request.query["newPrevTaskId"] == "7050"
    assert request.query["newNextTaskId"] == "7300"
    assert request.body == {}


# ---------------------------------------------------------------------------
# change_task_progress (распаковка result)
# ---------------------------------------------------------------------------


async def test_change_task_progress_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.change_task_progress(7200, progress=0.5)

    assert fake_ips.requests == []


async def test_change_task_progress_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/improjects/tasks/7200/changeProgress", body=_TASK_INFO_WRAP)
    async with _Client(config=token_config) as ips:
        info = await ips.change_task_progress(7200, progress=0.5, confirm=True)

    assert info["taskData"]["progress"] == 0.5
    assert info["projectId"] == 1500
    request = fake_ips.requests[-1]
    assert request.query["progress"] == "0.5"
    assert request.body == {}


# ---------------------------------------------------------------------------
# save_approval_result (тело + распаковка result)
# ---------------------------------------------------------------------------


async def test_save_approval_result_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.save_approval_result(7200, {"isApproved": True})

    assert fake_ips.requests == []


async def test_save_approval_result_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/improjects/tasks/7200/saveApprovalResult", body=_TASK_INFO_WRAP)
    async with _Client(config=token_config) as ips:
        info = await ips.save_approval_result(
            7200, {"isApproved": True, "managerMessage": "ok"}, confirm=True
        )

    assert info["projectId"] == 1500
    assert fake_ips.requests[-1].body == {"isApproved": True, "managerMessage": "ok"}


# ---------------------------------------------------------------------------
# start_executing_task / start_executing_project / stop_executing_project / complete_project
# ---------------------------------------------------------------------------


async def test_start_executing_task_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.start_executing_task(7200)

    assert fake_ips.requests == []


async def test_start_executing_task_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/improjects/tasks/7200/startExecuting", body=_TASK_INFO_WRAP)
    async with _Client(config=token_config) as ips:
        info = await ips.start_executing_task(7200, confirm=True)

    assert info["projectId"] == 1500
    assert fake_ips.requests[-1].body == {}


async def test_start_executing_project_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.start_executing_project(1500)

    assert fake_ips.requests == []


async def test_start_executing_project_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/improjects/project/1500/startExecuting", body=_STATUS_WRAP)
    async with _Client(config=token_config) as ips:
        res = await ips.start_executing_project(
            1500, is_need_to_log_modification_history=True, confirm=True
        )

    assert res["status"] == "executing"
    request = fake_ips.requests[-1]
    assert request.query["isNeedToLogModificationHistory"] == "true"
    assert request.body == {}


async def test_stop_executing_project_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.stop_executing_project(1500)

    assert fake_ips.requests == []


async def test_stop_executing_project_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    # Путь без слеша перед stopExecuting — особенность swagger.
    fake_ips.add("post", "/core/api/improjects/project/1500stopExecuting", body=_STATUS_WRAP)
    async with _Client(config=token_config) as ips:
        res = await ips.stop_executing_project(1500, confirm=True)

    assert res["status"] == "executing"
    assert fake_ips.requests[-1].path == "/core/api/improjects/project/1500stopExecuting"
    assert fake_ips.requests[-1].body == {}


async def test_complete_project_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.complete_project(1500)

    assert fake_ips.requests == []


async def test_complete_project_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/improjects/1500/completeProject", body=_TASK_INFO_WRAP)
    async with _Client(config=token_config) as ips:
        info = await ips.complete_project(1500, confirm=True)

    assert info["projectId"] == 1500
    assert fake_ips.requests[-1].body == {}


# ---------------------------------------------------------------------------
# save_project_zoom_level (query scaleType)
# ---------------------------------------------------------------------------


async def test_save_project_zoom_level_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.save_project_zoom_level(1500, scale_type=ScaleType.MONTHS)

    assert fake_ips.requests == []


async def test_save_project_zoom_level_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/improjects/1500/saveZoomLevel", body=_GANTT)
    async with _Client(config=token_config) as ips:
        res = await ips.save_project_zoom_level(1500, scale_type=ScaleType.MONTHS, confirm=True)

    assert res["action"]["type"] == "update"
    request = fake_ips.requests[-1]
    assert request.query["scaleType"] == "months"
    assert request.body == {}


# ---------------------------------------------------------------------------
# update_grid_columns (void)
# ---------------------------------------------------------------------------


async def test_update_grid_columns_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.update_grid_columns({"columns": []})

    assert fake_ips.requests == []


async def test_update_grid_columns_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/improjects/update-grid-columns", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.update_grid_columns(
            {"columns": [{"id": "text", "width": 200}]}, confirm=True
        )

    assert result is None
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.body == {"columns": [{"id": "text", "width": 200}]}
