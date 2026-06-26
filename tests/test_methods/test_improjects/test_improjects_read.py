"""Тесты методов чтения раздела управления проектами (Improject)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_PROJECT = {
    "id": 1500,
    "data": [{"id": 1, "text": "Задача 1"}],
    "links": [{"id": 10, "source": 1, "target": 2}],
    "resources": [{"id": 5, "text": "Иванов"}],
    "displaySettings": {"zoomLevel": "day"},
}

_TASK = {
    "projectId": 1500,
    "projectName": "Проект А",
    "managerAnswer": "Согласовано",
    "taskData": {"id": 7200, "text": "Задача", "progress": 0.5},
}

_ATTACHMENT = {
    "objectId": 102550,
    "id": 88,
    "typeId": 4,
    "objectTypeName": "Документ",
    "caption": "ТЗ.docx",
    "owner": 3,
    "ownerName": "Петров",
}

_ASSIGNMENTS = {
    "data": [{"id": 7200, "text": "Задача"}],
    "resources": [{"id": 5, "text": "Иванов"}],
    "users": [3, 7],
}


async def test_project_returns_project(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/improjects/1500", body=_PROJECT)
    async with IPSClient(config=token_config) as ips:
        proj = await ips.project(1500)

    assert proj.id == 1500
    assert proj.data == [{"id": 1, "text": "Задача 1"}]
    assert proj.links[0]["source"] == 1
    assert proj.resources[0]["text"] == "Иванов"
    assert proj.display_settings == {"zoomLevel": "day"}


async def test_project_coerces_null_collections(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {**_PROJECT, "data": None, "links": None, "resources": None, "displaySettings": None}
    fake_ips.add("get", "/core/api/improjects/1500", body=body)
    async with IPSClient(config=token_config) as ips:
        proj = await ips.project(1500)

    assert proj.data == []
    assert proj.links == []
    assert proj.resources == []
    assert proj.display_settings is None


async def test_task_returns_task(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/improjects/tasks/7200", body=_TASK)
    async with IPSClient(config=token_config) as ips:
        task = await ips.task(7200)

    assert task.project_id == 1500
    assert task.project_name == "Проект А"
    assert task.manager_answer == "Согласовано"
    assert task.task_data["progress"] == 0.5


async def test_task_attachments_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/improjects/tasks/7200/attachments",
        body=[_ATTACHMENT, _ATTACHMENT],
    )
    async with IPSClient(config=token_config) as ips:
        attachments = await ips.task_attachments(7200)

    assert len(attachments) == 2
    att = attachments[0]
    assert att.id == 88
    assert att.object_id == 102550
    assert att.type_id == 4
    assert att.object_type_name == "Документ"
    assert att.caption == "ТЗ.docx"
    assert att.owner == 3
    assert att.owner_name == "Петров"


async def test_resource_assignments_returns_assignments(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/improjects/resourceAssignments", body=_ASSIGNMENTS)
    async with IPSClient(config=token_config) as ips:
        assignments = await ips.resource_assignments()

    assert assignments.data[0]["id"] == 7200
    assert assignments.resources[0]["text"] == "Иванов"
    assert assignments.users == [3, 7]


async def test_resource_assignments_coerces_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/improjects/resourceAssignments", body={})
    async with IPSClient(config=token_config) as ips:
        assignments = await ips.resource_assignments()

    assert assignments.data == []
    assert assignments.resources == []
    assert assignments.users == []
