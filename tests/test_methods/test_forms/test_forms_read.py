"""Тесты методов чтения раздела форм (forms)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_GROUP = {
    "id": 5001,
    "versionID": 5002,
    "typeID": 1041,
    "caption": "Конструкторы",
}
_USER = {
    "id": 7001,
    "versionID": 7001,
    "typeID": 1040,
    "caption": "Иванов И.И.",
}
_COLOR = {
    "colorName": "Красный",
    "colorRGBA": "#FF0000FF",
    "a": 255,
    "r": 255,
    "g": 0,
    "b": 0,
}


async def test_find_user_groups_in_composition(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/findUserGroupsInComposition"
    fake_ips.add("get", path, body=[_GROUP, _GROUP])
    async with IPSClient(config=token_config) as ips:
        groups = await ips.find_user_groups_in_composition(102551)

    assert fake_ips.requests[-1].path == path
    assert len(groups) == 2
    assert groups[0].id == 5001
    assert groups[0].version_id == 5002
    assert groups[0].type_id == 1041
    assert groups[0].caption == "Конструкторы"


async def test_rank_find_inner_users(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/rankFindInnerUsersInComposition"
    fake_ips.add("get", path, body=[_USER])
    async with IPSClient(config=token_config) as ips:
        users = await ips.rank_find_inner_users(102551)

    assert fake_ips.requests[-1].path == path
    assert len(users) == 1
    assert users[0].id == 7001
    assert users[0].type_id == 1040
    assert users[0].caption == "Иванов И.И."


async def test_find_user_groups_and_users(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/findUserGroupsAndUsersInComposition"
    fake_ips.add("get", path, body={"userGroups": [_GROUP], "users": [_USER]})
    async with IPSClient(config=token_config) as ips:
        result = await ips.find_user_groups_and_users(102551)

    assert fake_ips.requests[-1].path == path
    assert len(result.user_groups) == 1
    assert result.user_groups[0].id == 5001
    assert len(result.users) == 1
    assert result.users[0].id == 7001


async def test_find_user_groups_and_users_coerces_null_lists(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = "/core/api/forms/findUserGroupsAndUsersInComposition"
    fake_ips.add("get", path, body={"userGroups": None, "users": None})
    async with IPSClient(config=token_config) as ips:
        result = await ips.find_user_groups_and_users(102551)

    assert result.user_groups == []
    assert result.users == []


async def test_widget_colors(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/getColors"
    fake_ips.add("get", path, body=[_COLOR])
    async with IPSClient(config=token_config) as ips:
        colors = await ips.widget_colors()

    assert fake_ips.requests[-1].path == path
    assert len(colors) == 1
    assert colors[0].color_name == "Красный"
    assert colors[0].color_rgba == "#FF0000FF"
    assert colors[0].r == 255
    assert colors[0].a == 255


async def test_system_colors(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/getSystemColors"
    fake_ips.add("get", path, body=[_COLOR, _COLOR])
    async with IPSClient(config=token_config) as ips:
        colors = await ips.system_colors()

    assert fake_ips.requests[-1].path == path
    assert len(colors) == 2
    assert colors[0].color_rgba == "#FF0000FF"
    assert colors[0].b == 0
