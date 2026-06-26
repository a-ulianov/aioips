"""Тесты read-методов объектов и параметров справочной системы IMBASE."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

ImBaseClient = IPSClient


# --- extendedItem (unwrap entity) ---------------------------------------------


async def test_imbase_extended_item_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/imbase/extendedItem/1029",
        body={
            "entity": {"catalogIds": [5, 6], "selectMode": "imcmSelectFolder"},
            "isEntityPresent": True,
        },
    )
    async with ImBaseClient(config=token_config) as ips:
        item = await ips.imbase_extended_item(1029)

    assert item is not None
    assert item.catalog_ids == [5, 6]
    assert item.select_mode == "imcmSelectFolder"


async def test_imbase_extended_item_null_entity_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/imbase/extendedItem/1029",
        body={"entity": None, "isEntityPresent": False},
    )
    async with ImBaseClient(config=token_config) as ips:
        item = await ips.imbase_extended_item(1029)

    assert item is None


# --- object path family (unwrap entity) ---------------------------------------

_PATH_BODY = {
    "entity": {
        "topParentObjectId": 100,
        "topParentCatalogType": "catalog",
        "path": ["100", "200", "300"],
        "objectsPath": [{"objectId": 100, "relationId": None}],
        "recordId": 42,
        "objectId": 300,
    },
    "isEntityPresent": True,
}


async def test_imbase_object_path_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/imbase/object/300/path", body=_PATH_BODY)
    async with ImBaseClient(config=token_config) as ips:
        path = await ips.imbase_object_path(300)

    assert path is not None
    assert path.top_parent_object_id == 100
    assert path.path == ["100", "200", "300"]
    assert path.objects_path[0]["objectId"] == 100
    assert path.record_id == 42
    assert path.object_id == 300


async def test_imbase_object_path_null_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/imbase/object/300/path",
        body={"entity": None, "isEntityPresent": False},
    )
    async with ImBaseClient(config=token_config) as ips:
        path = await ips.imbase_object_path(300)

    assert path is None


async def test_imbase_linked_object_path_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/imbase/linkedObject/300/path", body=_PATH_BODY)
    async with ImBaseClient(config=token_config) as ips:
        path = await ips.imbase_linked_object_path(300)

    assert path is not None
    assert path.object_id == 300


async def test_imbase_object_path_by_key_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/imbase/object/byKey/777/path", body=_PATH_BODY)
    async with ImBaseClient(config=token_config) as ips:
        path = await ips.imbase_object_path_by_key(777)

    assert path is not None
    assert path.top_parent_catalog_type == "catalog"


# --- text note (scalar str) ---------------------------------------------------


async def test_imbase_text_note_by_guid_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    guid = "cad001c5-306c-11d8-b4e9-00304f19f545"
    fake_ips.add(
        "get",
        f"/core/api/imbase/object/textNote/byGuid/{guid}",
        body="заметка к записи",
    )
    async with ImBaseClient(config=token_config) as ips:
        note = await ips.imbase_text_note_by_guid(guid)

    assert note == "заметка к записи"


# --- create info (schema, no wrapper) -----------------------------------------


async def test_imbase_object_create_info_parses(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/imbase/object/555/createInfo",
        body={
            "shouldCreateNewObject": True,
            "objectTypeId": 1742,
            "existingObjects": [11, 22],
        },
    )
    async with ImBaseClient(config=token_config) as ips:
        info = await ips.imbase_object_create_info(555)

    assert info.should_create_new_object is True
    assert info.object_type_id == 1742
    assert info.existing_objects == [11, 22]


# --- scalars: catalog id / favorite count -------------------------------------


async def test_imbase_catalog_id_by_object_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/imbase/object/300/catalog/id", body=100)
    async with ImBaseClient(config=token_config) as ips:
        catalog_id = await ips.imbase_catalog_id_by_object(300)

    assert catalog_id == 100


async def test_imbase_favorite_folders_count_returns_int(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/imbase/object/300/favoriteFoldersCount", body=3)
    async with ImBaseClient(config=token_config) as ips:
        count = await ips.imbase_favorite_folders_count(300)

    assert count == 3


# --- applicability (unwrap) / restrictive cache (bool) ------------------------


async def test_imbase_object_applicability_unwraps_entity(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/imbase/object/7700/applicability",
        body={
            "entity": {
                "applicabilityStatus": "limitedUse",
                "positionInRestrictionList": True,
            },
            "isEntityPresent": True,
        },
    )
    async with ImBaseClient(config=token_config) as ips:
        result = await ips.imbase_object_applicability(7700)

    assert result is not None
    assert result.applicability_status == "limitedUse"
    assert result.position_in_restriction_list is True


async def test_imbase_object_applicability_null_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/imbase/object/7700/applicability",
        body={"entity": None, "isEntityPresent": False},
    )
    async with ImBaseClient(config=token_config) as ips:
        result = await ips.imbase_object_applicability(7700)

    assert result is None


async def test_imbase_restrictive_applicability_cache_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/imbase/object/7700/applicability/restrictiveCache",
        body=True,
    )
    async with ImBaseClient(config=token_config) as ips:
        cached = await ips.imbase_restrictive_applicability_cache(7700)

    assert cached is True


# --- params (raw dict, corrupted-key DTO) -------------------------------------


async def test_imbase_common_params_returns_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {
        "deleteRecordMode": "disable",
        "denyFewLinksForSameTable": False,
        "checkApplicabilityBeforeCreateComposition": True,
    }
    fake_ips.add("get", "/core/api/imbase/params/common", body=body)
    async with ImBaseClient(config=token_config) as ips:
        params = await ips.imbase_common_params()

    assert params["deleteRecordMode"] == "disable"
    assert params["checkApplicabilityBeforeCreateComposition"] is True


async def test_imbase_user_params_returns_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {"hideEmptyColumns": False, "freezeFirstColumn": True}
    fake_ips.add("get", "/core/api/imbase/params/user", body=body)
    async with ImBaseClient(config=token_config) as ips:
        params = await ips.imbase_user_params()

    assert params["hideEmptyColumns"] is False
    assert params["freezeFirstColumn"] is True


# --- role display modes (list of schema) / terminal folders (list[int]) -------


async def test_imbase_role_display_mode_options_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    body = [
        {
            "objectId": "cad001c5-306c-11d8-b4e9-00304f19f545",
            "objectVersionId": 7,
            "name": "Конструктор",
        }
    ]
    fake_ips.add("get", "/core/api/imbase/roleDisplayModeOptions", body=body)
    async with ImBaseClient(config=token_config) as ips:
        roles = await ips.imbase_role_display_mode_options()

    assert len(roles) == 1
    assert roles[0].object_version_id == 7
    assert roles[0].name == "Конструктор"


async def test_imbase_terminal_folder_ids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/imbase/terminalFolders", body=[101, 102, 103])
    async with ImBaseClient(config=token_config) as ips:
        folder_ids = await ips.imbase_terminal_folder_ids()

    assert folder_ids == [101, 102, 103]
