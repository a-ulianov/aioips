"""Тесты скалярных методов дерева типов объектов (objectTypeTree) раздела metadata.

Проверяют построение пути запроса и преобразование возврата для каждого метода
(списки int/str, скаляры int/str/bool), включая пустой ответ (``None`` → []/0/""/False)
и URL-кодирование GUID на byGuid-путях (quote(safe="")).
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"
# GUID с символами, требующими кодирования в URL (для проверки quote(safe="")).
_GUID_NEEDS_QUOTE = "a b/c"

_TREE = "/core/api/metadata/objectTypeTree"


# --- children: по id родителя ---


async def test_children_type_ids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/children/1742/ids", body=[10, 11])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.children_type_ids(1742)

    assert ids == [10, 11]
    assert all(isinstance(i, int) for i in ids)


async def test_children_type_ids_empty_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/children/1742/ids", body=None)
    async with IPSClient(config=token_config) as ips:
        ids = await ips.children_type_ids(1742)

    assert ids == []


async def test_children_type_guids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/children/1742/guids", body=[_GUID])
    async with IPSClient(config=token_config) as ips:
        guids = await ips.children_type_guids(1742)

    assert guids == [_GUID]
    assert all(isinstance(g, str) for g in guids)


# --- children: по GUID родителя (проверка кодирования) ---


async def test_children_type_ids_by_guid_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/children/byGuid/{_GUID}/ids", body=[10])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.children_type_ids_by_guid(_GUID)

    assert ids == [10]


async def test_children_type_ids_by_guid_encodes_guid(token_config: IPSConfig, fake_ips: FakeIPS):
    # FakeIPS видит уже декодированный путь — значит quote(safe="") отработал.
    fake_ips.add("get", f"{_TREE}/children/byGuid/{_GUID_NEEDS_QUOTE}/ids", body=[1])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.children_type_ids_by_guid(_GUID_NEEDS_QUOTE)

    assert ids == [1]


async def test_children_type_guids_by_guid_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/children/byGuid/{_GUID}/guids", body=[_GUID])
    async with IPSClient(config=token_config) as ips:
        guids = await ips.children_type_guids_by_guid(_GUID)

    assert guids == [_GUID]


async def test_children_type_guids_by_guid_encodes_guid(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/children/byGuid/{_GUID_NEEDS_QUOTE}/guids", body=[_GUID])
    async with IPSClient(config=token_config) as ips:
        guids = await ips.children_type_guids_by_guid(_GUID_NEEDS_QUOTE)

    assert guids == [_GUID]


# --- children: рекурсивно ---


async def test_children_type_ids_recursive_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/children/1742/recursive/ids", body=[10, 20, 30])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.children_type_ids_recursive(1742)

    assert ids == [10, 20, 30]


async def test_children_type_guids_recursive_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", f"{_TREE}/children/1742/recursive/guids", body=[_GUID])
    async with IPSClient(config=token_config) as ips:
        guids = await ips.children_type_guids_recursive(1742)

    assert guids == [_GUID]


async def test_children_type_ids_recursive_by_guid_encodes_guid(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", f"{_TREE}/children/byGuid/{_GUID_NEEDS_QUOTE}/recursive/ids", body=[5, 6])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.children_type_ids_recursive_by_guid(_GUID_NEEDS_QUOTE)

    assert ids == [5, 6]


async def test_children_type_guids_recursive_by_guid_encodes_guid(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get", f"{_TREE}/children/byGuid/{_GUID_NEEDS_QUOTE}/recursive/guids", body=[_GUID]
    )
    async with IPSClient(config=token_config) as ips:
        guids = await ips.children_type_guids_recursive_by_guid(_GUID_NEEDS_QUOTE)

    assert guids == [_GUID]


async def test_local_children_type_ids_recursive_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", f"{_TREE}/children/1742/local/recursive/ids", body=[7])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.local_children_type_ids_recursive(1742)

    assert ids == [7]


# --- parent: непосредственный ---


async def test_parent_type_id_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/parent/1742/id", body=1700)
    async with IPSClient(config=token_config) as ips:
        parent_id = await ips.parent_type_id(1742)

    assert parent_id == 1700
    assert isinstance(parent_id, int)


async def test_parent_type_id_zero_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/parent/1742/id", body=None)
    async with IPSClient(config=token_config) as ips:
        parent_id = await ips.parent_type_id(1742)

    assert parent_id == 0


async def test_parent_type_guid_by_guid_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/parent/byGuid/{_GUID}/guid", body=_GUID)
    async with IPSClient(config=token_config) as ips:
        guid = await ips.parent_type_guid_by_guid(_GUID)

    assert guid == _GUID


async def test_parent_type_guid_by_guid_empty_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/parent/byGuid/{_GUID_NEEDS_QUOTE}/guid", body=None)
    async with IPSClient(config=token_config) as ips:
        guid = await ips.parent_type_guid_by_guid(_GUID_NEEDS_QUOTE)

    assert guid == ""


# --- parents: вся цепочка ---


async def test_parent_type_ids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/parents/1742/ids", body=[1700, 1600])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.parent_type_ids(1742)

    assert ids == [1700, 1600]


async def test_parent_type_guids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/parents/1742/guids", body=[_GUID])
    async with IPSClient(config=token_config) as ips:
        guids = await ips.parent_type_guids(1742)

    assert guids == [_GUID]


async def test_parent_type_ids_by_guid_encodes_guid(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/parents/byGuid/{_GUID_NEEDS_QUOTE}/ids", body=[1700])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.parent_type_ids_by_guid(_GUID_NEEDS_QUOTE)

    assert ids == [1700]


async def test_parent_type_guids_by_guid_encodes_guid(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/parents/byGuid/{_GUID_NEEDS_QUOTE}/guids", body=[_GUID])
    async with IPSClient(config=token_config) as ips:
        guids = await ips.parent_type_guids_by_guid(_GUID_NEEDS_QUOTE)

    assert guids == [_GUID]


async def test_parent_type_ids_reverse_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/parents/1742/ids/reverse", body=[1600, 1700])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.parent_type_ids_reverse(1742)

    assert ids == [1600, 1700]


# --- topParent / commonParent ---


async def test_top_parent_type_id_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/topParent/1742/id", body=1600)
    async with IPSClient(config=token_config) as ips:
        root_id = await ips.top_parent_type_id(1742)

    assert root_id == 1600


async def test_common_parent_type_id_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/commonParent/1742/1801/id", body=1600)
    async with IPSClient(config=token_config) as ips:
        common_id = await ips.common_parent_type_id(1742, 1801)

    assert common_id == 1600
    assert isinstance(common_id, int)


# --- isChild ---


async def test_is_object_type_child_true(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/isChild/byChildId/1742/byParentId/1700", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.is_object_type_child(1742, 1700)

    assert result is True


async def test_is_object_type_child_false_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/isChild/byChildId/1742/byParentId/1700", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.is_object_type_child(1742, 1700)

    assert result is False


async def test_is_object_type_child_by_child_id_parent_guid_encodes_guid(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"{_TREE}/isChild/byChildId/1742/byParentGuid/{_GUID_NEEDS_QUOTE}",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.is_object_type_child_by_child_id_parent_guid(1742, _GUID_NEEDS_QUOTE)

    assert result is True


async def test_is_object_type_child_by_guids_encodes_both_guids(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"{_TREE}/isChild/byChildGuid/{_GUID_NEEDS_QUOTE}/byParentGuid/{_GUID}",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.is_object_type_child_by_guids(_GUID_NEEDS_QUOTE, _GUID)

    assert result is True


# --- objectTypeLevel / topObjectTypes ---


async def test_object_type_level_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/objectTypeLevel/1742", body=3)
    async with IPSClient(config=token_config) as ips:
        level = await ips.object_type_level(1742)

    assert level == 3
    assert isinstance(level, int)


async def test_object_type_level_zero_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/objectTypeLevel/1742", body=None)
    async with IPSClient(config=token_config) as ips:
        level = await ips.object_type_level(1742)

    assert level == 0


async def test_top_object_type_ids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/topObjectTypes/ids", body=[1600, 1601])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.top_object_type_ids()

    assert ids == [1600, 1601]


async def test_top_object_type_guids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"{_TREE}/topObjectTypes/guids", body=[_GUID])
    async with IPSClient(config=token_config) as ips:
        guids = await ips.top_object_type_guids()

    assert guids == [_GUID]
