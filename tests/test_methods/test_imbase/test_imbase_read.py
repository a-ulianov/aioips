"""Тесты методов чтения раздела справочной системы IMBASE."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

ImBaseClient = IPSClient


async def test_imbase_catalogs_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/imbase/catalogs",
        body={"entity": [10, 20, 30], "isEntityPresent": True},
    )
    async with ImBaseClient(config=token_config) as ips:
        catalogs = await ips.imbase_catalogs()

    assert catalogs == [10, 20, 30]


async def test_imbase_catalogs_null_entity_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/imbase/catalogs",
        body={"entity": None, "isEntityPresent": False},
    )
    async with ImBaseClient(config=token_config) as ips:
        catalogs = await ips.imbase_catalogs()

    assert catalogs is None


async def test_imbase_supported_catalogs_passes_query(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/imbase/catalogs/supported", body=[1742, 1743])
    async with ImBaseClient(config=token_config) as ips:
        catalogs = await ips.imbase_supported_catalogs(object_type_id=1742, attribute_type_id=1029)

    assert catalogs == [1742, 1743]
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/imbase/catalogs/supported"


async def test_imbase_client_cache_state_parses(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {
        "displayModeOptions": [{"mode": "generalMode", "name": "Общий"}],
        "roleDisplayModeOptions": [
            {"objectId": "cad001c5-306c-11d8-b4e9-00304f19f545", "objectVersionId": 7, "name": "R"}
        ],
        "commonParams": {"deleteRecordMode": "disable"},
        "userParams": {"hideEmptyColumns": False},
        "terminalFolderIds": [101, 102],
        "indexesInfo": {
            "catalogs": [{"id": 5, "name": "Материалы", "type": "catalog"}],
            "indexes": [{"catalogId": 5, "attributeId": 1029}],
        },
    }
    fake_ips.add("get", "/core/api/imbase/clientCacheState", body=body)
    async with ImBaseClient(config=token_config) as ips:
        state = await ips.imbase_client_cache_state()

    assert state.terminal_folder_ids == [101, 102]
    assert state.display_mode_options[0].mode == "generalMode"
    assert state.display_mode_options[0].name == "Общий"
    assert state.common_params["deleteRecordMode"] == "disable"
    assert state.user_params["hideEmptyColumns"] is False
    assert state.role_display_mode_options[0]["objectVersionId"] == 7
    assert state.indexes_info.catalogs[0].id == 5
    assert state.indexes_info.indexes[0].catalog_id == 5
    assert state.indexes_info.indexes[0].attribute_id == 1029


async def test_imbase_client_cache_state_coerces_null_lists(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    body = {
        "displayModeOptions": None,
        "roleDisplayModeOptions": None,
        "commonParams": {},
        "userParams": {},
        "terminalFolderIds": None,
        "indexesInfo": {"catalogs": None, "indexes": None},
    }
    fake_ips.add("get", "/core/api/imbase/clientCacheState", body=body)
    async with ImBaseClient(config=token_config) as ips:
        state = await ips.imbase_client_cache_state()

    assert state.display_mode_options == []
    assert state.role_display_mode_options == []
    assert state.terminal_folder_ids == []
    assert state.indexes_info.catalogs == []
    assert state.indexes_info.indexes == []


async def test_imbase_display_mode_options_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    body = [
        {"mode": "generalMode", "name": "Общий"},
        {"mode": "personalMode", "name": "Персональный"},
    ]
    fake_ips.add("get", "/core/api/imbase/displayModeOptions", body=body)
    async with ImBaseClient(config=token_config) as ips:
        modes = await ips.imbase_display_mode_options()

    assert len(modes) == 2
    assert modes[1].mode == "personalMode"
    assert modes[1].name == "Персональный"


async def test_imbase_indexes_parses_nested(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {
        "catalogs": [{"id": 5, "name": "Материалы", "type": "catalog"}],
        "indexes": [{"catalogId": 5, "attributeId": 1029}],
    }
    fake_ips.add("get", "/core/api/imbase/indexes", body=body)
    async with ImBaseClient(config=token_config) as ips:
        info = await ips.imbase_indexes()

    assert info.catalogs[0].id == 5
    assert info.catalogs[0].name == "Материалы"
    assert info.catalogs[0].type == "catalog"
    assert info.indexes[0].catalog_id == 5
    assert info.indexes[0].attribute_id == 1029
