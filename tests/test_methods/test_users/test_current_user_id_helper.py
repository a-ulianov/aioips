"""Тест метода «помощник идентификаторов» текущего пользователя."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_ID_HELPER = {
    "nameID": 1001,
    "designationID": 1002,
    "shortNameID": 1003,
    "usersTypeID": 2,
    "groupsTypeID": 3,
    "rolesTypeID": 4,
    "allUsersGroupID": 500,
    "adminRoleID": 600,
    "sysdbaID": 1,
    "defaultLanguageID": "ru-RU",
    "compositionVersionBackup": 77,
}


async def test_current_user_id_helper_parses_ids(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/currentUsers/GetIdHelper", body=_ID_HELPER)
    async with IPSClient(config=token_config) as ips:
        ids = await ips.id_helper()

    # Проверяем явные алиасы с акронимом ID в верхнем регистре.
    assert ids.name_id == 1001
    assert ids.designation_id == 1002
    assert ids.short_name_id == 1003
    assert ids.users_type_id == 2
    assert ids.all_users_group_id == 500
    assert ids.admin_role_id == 600
    assert ids.sysdba_id == 1
    # Строковый идентификатор языка.
    assert ids.default_language_id == "ru-RU"
    # Поле без суффикса ID (обычный camelCase).
    assert ids.composition_version_backup == 77


async def test_current_user_id_helper_allows_partial(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/currentUsers/GetIdHelper", body={"nameID": 1001})
    async with IPSClient(config=token_config) as ips:
        ids = await ips.id_helper()

    assert ids.name_id == 1001
    # Непришедшие поля — None.
    assert ids.designation_id is None
    assert ids.all_users_group_id is None
