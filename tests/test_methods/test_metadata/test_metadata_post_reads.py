"""Тесты POST-методов ЧТЕНИЯ раздела metadata.

Проверяют для каждого метода: путь запроса, тело (JSON-список/словарь, попадающее
на сервер), HTTP-глагол POST и преобразование возврата, включая распаковку
``*NullableResultDto`` (``entity``/``isEntityPresent``) в список либо ``None``,
скаляры int/bool и табличный ``DataTableDto``.
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient

_GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"
_REL_GUID = "11111111-2222-3333-4444-555555555555"
_META = "/core/api/metadata"
_APPLIC = f"{_META}/applicabilities/childObjectTypes"
_TREE = f"{_META}/objectTypeTree"


# --- applicability child object types по нескольким связям ---


async def test_child_guids_by_parent_guid_relation_guids_unwraps_entity(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = f"{_APPLIC}/byGuids/{_GUID}/guids"
    fake_ips.add("post", path, body={"entity": [_GUID], "isEntityPresent": True})
    async with _Client(config=token_config) as ips:
        guids = await ips.applicability_child_object_type_guids_by_parent_guid_relation_guids(
            _GUID, [_REL_GUID]
        )

    assert guids == [_GUID]
    captured = fake_ips.requests[-1]
    assert captured.method == "POST"
    assert captured.path == path
    assert captured.body == [_REL_GUID]


async def test_child_guids_by_parent_guid_relation_guids_none_when_absent(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = f"{_APPLIC}/byGuids/{_GUID}/guids"
    fake_ips.add("post", path, body={"entity": None, "isEntityPresent": False})
    async with _Client(config=token_config) as ips:
        guids = await ips.applicability_child_object_type_guids_by_parent_guid_relation_guids(
            _GUID, [_REL_GUID]
        )

    assert guids is None


async def test_child_ids_by_parent_guid_relation_guids_unwraps_entity(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = f"{_APPLIC}/byGuids/{_GUID}/ids"
    fake_ips.add("post", path, body={"entity": [10, 11], "isEntityPresent": True})
    async with _Client(config=token_config) as ips:
        ids = await ips.applicability_child_object_type_ids_by_parent_guid_relation_guids(
            _GUID, [_REL_GUID]
        )

    assert ids == [10, 11]
    assert all(isinstance(i, int) for i in ids)
    assert fake_ips.requests[-1].body == [_REL_GUID]


async def test_child_ids_by_parent_guid_relation_guids_none_when_absent(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = f"{_APPLIC}/byGuids/{_GUID}/ids"
    fake_ips.add("post", path, body={"entity": None, "isEntityPresent": False})
    async with _Client(config=token_config) as ips:
        ids = await ips.applicability_child_object_type_ids_by_parent_guid_relation_guids(
            _GUID, [_REL_GUID]
        )

    assert ids is None


async def test_child_guids_by_parent_id_relation_ids_unwraps_entity(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = f"{_APPLIC}/byIds/1742/guids"
    fake_ips.add("post", path, body={"entity": [_GUID], "isEntityPresent": True})
    async with _Client(config=token_config) as ips:
        guids = await ips.applicability_child_object_type_guids_by_parent_id_relation_ids(
            1742, [501, 502]
        )

    assert guids == [_GUID]
    assert fake_ips.requests[-1].body == [501, 502]


async def test_child_guids_by_parent_id_relation_ids_none_when_absent(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = f"{_APPLIC}/byIds/1742/guids"
    fake_ips.add("post", path, body={"entity": None, "isEntityPresent": False})
    async with _Client(config=token_config) as ips:
        guids = await ips.applicability_child_object_type_guids_by_parent_id_relation_ids(
            1742, [501]
        )

    assert guids is None


# --- isEnabledParentType ---


async def test_is_enabled_parent_type_true(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"{_META}/applicabilities/isEnabledParentType/1742"
    fake_ips.add("post", path, body=True)
    async with _Client(config=token_config) as ips:
        result = await ips.is_enabled_parent_type(
            1742, enabled_parent_type_ids=[1700], disabled_parent_type_ids=[]
        )

    assert result is True
    captured = fake_ips.requests[-1]
    assert captured.method == "POST"
    assert captured.body == {"enabledParentTypeIds": [1700], "disabledParentTypeIds": []}
    assert captured.query.get("defaultValue") == "false"


async def test_is_enabled_parent_type_false_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"{_META}/applicabilities/isEnabledParentType/1742"
    fake_ips.add("post", path, body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.is_enabled_parent_type(
            1742,
            enabled_parent_type_ids=[],
            disabled_parent_type_ids=[1700],
            default_value=True,
        )

    assert result is False
    assert fake_ips.requests[-1].query.get("defaultValue") == "true"


# --- filters ---


async def test_metadata_filters_returns_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", f"{_META}/filters", body={"Документы": [10, 11], "Изделия": [20]})
    async with _Client(config=token_config) as ips:
        filters = await ips.metadata_filters(["Документы", "Изделия"])

    assert filters == {"Документы": [10, 11], "Изделия": [20]}
    assert fake_ips.requests[-1].body == ["Документы", "Изделия"]


async def test_metadata_filters_empty_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", f"{_META}/filters", body=None)
    async with _Client(config=token_config) as ips:
        filters = await ips.metadata_filters(["X"])

    assert filters == {}


# --- objectTypeTree children recursive ---


async def test_children_guids_recursive_by_guids_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = f"{_TREE}/children/byGuids/recursive/guids"
    fake_ips.add("post", path, body=[_GUID])
    async with _Client(config=token_config) as ips:
        guids = await ips.object_type_children_guids_recursive_by_guids([_GUID])

    assert guids == [_GUID]
    assert fake_ips.requests[-1].body == [_GUID]


async def test_children_guids_recursive_by_guids_empty_when_null(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = f"{_TREE}/children/byGuids/recursive/guids"
    fake_ips.add("post", path, body=None)
    async with _Client(config=token_config) as ips:
        guids = await ips.object_type_children_guids_recursive_by_guids([_GUID])

    assert guids == []


async def test_local_children_ids_recursive_by_ids_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = f"{_TREE}/children/byIds/local/recursive/ids"
    fake_ips.add("post", path, body=[7, 8])
    async with _Client(config=token_config) as ips:
        ids = await ips.local_object_type_children_ids_recursive_by_ids([1742])

    assert ids == [7, 8]
    assert fake_ips.requests[-1].body == [1742]


async def test_children_ids_recursive_by_ids_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = f"{_TREE}/children/byIds/recursive/ids"
    fake_ips.add("post", path, body=[10, 20, 30])
    async with _Client(config=token_config) as ips:
        ids = await ips.object_type_children_ids_recursive_by_ids([1742, 1801])

    assert ids == [10, 20, 30]
    assert fake_ips.requests[-1].body == [1742, 1801]


# --- commonParent ---


async def test_common_parent_id_by_ids_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", f"{_TREE}/commonParent/byIds/id", body=1600)
    async with _Client(config=token_config) as ips:
        common_id = await ips.common_parent_object_type_id_by_ids([1742, 1801])

    assert common_id == 1600
    assert isinstance(common_id, int)
    assert fake_ips.requests[-1].body == [1742, 1801]


async def test_common_parent_id_by_ids_zero_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", f"{_TREE}/commonParent/byIds/id", body=None)
    async with _Client(config=token_config) as ips:
        common_id = await ips.common_parent_object_type_id_by_ids([1742])

    assert common_id == 0


async def test_common_parent_id_by_version_ids_returns_int(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", f"{_TREE}/commonParent/byVersionIds/id", body=1600)
    async with _Client(config=token_config) as ips:
        common_id = await ips.common_parent_object_type_id_by_version_ids([102550, 102551])

    assert common_id == 1600
    assert fake_ips.requests[-1].body == [102550, 102551]


# --- optimize / topParents ---


async def test_optimize_child_object_types_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", f"{_TREE}/optimizeChildObjectTypes", body=[1700])
    async with _Client(config=token_config) as ips:
        minimal = await ips.optimize_child_object_types([1700, 1742])

    assert minimal == [1700]
    assert fake_ips.requests[-1].body == [1700, 1742]


async def test_top_parent_enabled_guids_by_guids_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", f"{_TREE}/topParents/byGuids/guids", body=[_GUID])
    async with _Client(config=token_config) as ips:
        roots = await ips.top_parent_enabled_object_type_guids_by_guids([_GUID])

    assert roots == [_GUID]
    assert fake_ips.requests[-1].body == [_GUID]


async def test_top_parent_enabled_ids_by_ids_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", f"{_TREE}/topParents/byIds/ids", body=[1600])
    async with _Client(config=token_config) as ips:
        roots = await ips.top_parent_enabled_object_type_ids_by_ids([1742, 1801])

    assert roots == [1600]
    assert fake_ips.requests[-1].body == [1742, 1801]


# --- hasLocal ---


async def test_has_local_object_type_true(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", f"{_META}/objectTypes/hasLocal", body=True)
    async with _Client(config=token_config) as ips:
        result = await ips.has_local_object_type([1742, 1801])

    assert result is True
    assert fake_ips.requests[-1].body == [1742, 1801]


async def test_has_local_object_type_false_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", f"{_META}/objectTypes/hasLocal", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.has_local_object_type([1742])

    assert result is False


# --- select ---


async def test_metadata_select_returns_data_table(token_config: IPSConfig, fake_ips: FakeIPS):
    request = {
        "tableName": "T_OBJECT_TYPES",
        "resultColumns": ["F_ID", "F_NAME"],
        "whereEquals": {"F_LOCAL": 1},
    }
    fake_ips.add(
        "post",
        f"{_META}/select",
        body={"columns": ["F_ID", "F_NAME"], "rows": [[1742, "Деталь"]]},
    )
    async with _Client(config=token_config) as ips:
        table = await ips.metadata_select(request)

    assert table.columns == ["F_ID", "F_NAME"]
    assert table.rows == [[1742, "Деталь"]]
    captured = fake_ips.requests[-1]
    assert captured.method == "POST"
    assert captured.body == request


async def test_metadata_select_empty_when_null_fields(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", f"{_META}/select", body={"columns": None, "rows": None})
    async with _Client(config=token_config) as ips:
        table = await ips.metadata_select({"tableName": "T"})

    assert table.columns == []
    assert table.rows == []


# --- state ---


async def test_metadata_state_returns_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {"imsObjectTypes": [{"id": 1742}], "lastUpdateDates": {"objectTypes": "2026-01-01"}}
    fake_ips.add("post", f"{_META}/state", body=body)
    async with _Client(config=token_config) as ips:
        state = await ips.metadata_state({}, partial_fetch_mode=True)

    assert state == body
    captured = fake_ips.requests[-1]
    assert captured.method == "POST"
    assert captured.body == {}
    assert captured.query.get("partialFetchMode") == "true"


async def test_metadata_state_empty_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", f"{_META}/state", body=None)
    async with _Client(config=token_config) as ips:
        state = await ips.metadata_state({"objectTypes": "2026-01-01"})

    assert state == {}
    assert fake_ips.requests[-1].query.get("partialFetchMode") == "false"
