"""Тесты скалярных методов группировки и сортировки раздела metadata.

Проверяют построение пути запроса и преобразование возврата для каждого
метода (списки int/str и булевы флаги), включая пустой ответ (``None`` → []/False).
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"


# --- grouping: объекты (groupable) ---


async def test_groupable_object_type_ids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/grouping/objectTypes/groupable/ids", body=[1, 2, 3])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.groupable_object_type_ids()

    assert ids == [1, 2, 3]
    assert all(isinstance(i, int) for i in ids)
    assert fake_ips.requests[-1].path == ("/core/api/metadata/grouping/objectTypes/groupable/ids")


async def test_groupable_object_type_ids_empty_when_null(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/grouping/objectTypes/groupable/ids", body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.groupable_object_type_ids() == []


async def test_groupable_object_type_guids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/grouping/objectTypes/groupable/guids", body=[_GUID])
    async with IPSClient(config=token_config) as ips:
        guids = await ips.groupable_object_type_guids()

    assert guids == [_GUID]
    assert all(isinstance(g, str) for g in guids)


async def test_object_type_is_groupable_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/grouping/objectTypes/groupable/42/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_type_is_groupable(42) is True


async def test_object_type_is_groupable_false_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/grouping/objectTypes/groupable/99/exists", body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_type_is_groupable(99) is False


async def test_object_type_is_groupable_by_guid_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/grouping/objectTypes/groupable/byGuid/{_GUID}/exists",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_type_is_groupable_by_guid(_GUID) is True


# --- grouping: объекты (grouping) ---


async def test_grouping_object_type_ids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/grouping/objectTypes/grouping/ids", body=[10, 20])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.grouping_object_type_ids()

    assert ids == [10, 20]
    assert all(isinstance(i, int) for i in ids)


async def test_grouping_object_type_guids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/grouping/objectTypes/grouping/guids", body=[_GUID])
    async with IPSClient(config=token_config) as ips:
        assert await ips.grouping_object_type_guids() == [_GUID]


async def test_object_type_has_grouping_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/grouping/objectTypes/grouping/42/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_type_has_grouping(42) is True


async def test_object_type_has_grouping_by_guid_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/grouping/objectTypes/grouping/byGuid/{_GUID}/exists",
        body=False,
    )
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_type_has_grouping_by_guid(_GUID) is False


# --- grouping: типы связей ---


async def test_grouping_relation_type_ids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/grouping/relationTypes/ids", body=[7])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.grouping_relation_type_ids()

    assert ids == [7]
    assert all(isinstance(i, int) for i in ids)


async def test_grouping_relation_type_guids_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/grouping/relationTypes/guids", body=[_GUID])
    async with IPSClient(config=token_config) as ips:
        assert await ips.grouping_relation_type_guids() == [_GUID]


async def test_relation_type_has_grouping_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/grouping/relationTypes/7/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        assert await ips.relation_type_has_grouping(7) is True


async def test_relation_type_has_grouping_by_guid_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", f"/core/api/metadata/grouping/relationTypes/{_GUID}/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        assert await ips.relation_type_has_grouping_by_guid(_GUID) is True


# --- sorting: объекты ---


async def test_sorting_object_type_ids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/sorting/objectTypes/ids", body=[1, 5])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.sorting_object_type_ids()

    assert ids == [1, 5]
    assert all(isinstance(i, int) for i in ids)


async def test_sorting_object_type_guids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/sorting/objectTypes/guids", body=[_GUID])
    async with IPSClient(config=token_config) as ips:
        assert await ips.sorting_object_type_guids() == [_GUID]


async def test_object_type_has_sorting_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/sorting/objectTypes/42/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_type_has_sorting(42) is True


async def test_object_type_has_sorting_false_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/sorting/objectTypes/99/exists", body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_type_has_sorting(99) is False


async def test_object_type_has_sorting_by_guid_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/sorting/objectTypes/byGuid/{_GUID}/exists",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_type_has_sorting_by_guid(_GUID) is True


# --- sorting: типы связей ---


async def test_sorting_relation_type_ids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/sorting/relationTypes/ids", body=[3, 4])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.sorting_relation_type_ids()

    assert ids == [3, 4]
    assert all(isinstance(i, int) for i in ids)


async def test_sorting_relation_type_guids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/sorting/relationTypes/guids", body=[_GUID])
    async with IPSClient(config=token_config) as ips:
        assert await ips.sorting_relation_type_guids() == [_GUID]


async def test_relation_type_has_sorting_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/sorting/relationTypes/7/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        assert await ips.relation_type_has_sorting(7) is True


async def test_relation_type_has_sorting_by_guid_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/sorting/relationTypes/byGuid/{_GUID}/exists",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        assert await ips.relation_type_has_sorting_by_guid(_GUID) is True
