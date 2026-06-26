"""Тесты скалярных методов разделов design, visibility и pdm раздела metadata.

Проверяют построение пути запроса и преобразование возврата для каждого метода
(списки int/str и булевы флаги), включая пустой ответ (``None`` → []/False) и
URL-кодирование GUID в byGuid-вариантах.
"""

from urllib.parse import quote

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"
_ENC = quote(_GUID, safe="")


# --- design ---


async def test_designed_object_type_ids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/design/objectTypes/ids", body=[1, 2, 3])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.designed_object_type_ids()

    assert ids == [1, 2, 3]
    assert all(isinstance(i, int) for i in ids)
    assert fake_ips.requests[-1].path == "/core/api/metadata/design/objectTypes/ids"


async def test_designed_object_type_ids_empty_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/design/objectTypes/ids", body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.designed_object_type_ids() == []


async def test_designed_object_type_guids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/design/objectTypes/guids", body=[_GUID])
    async with IPSClient(config=token_config) as ips:
        guids = await ips.designed_object_type_guids()

    assert guids == [_GUID]
    assert all(isinstance(g, str) for g in guids)


async def test_object_type_has_design_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/design/objectTypes/42/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_type_has_design(42) is True


async def test_object_type_has_design_false_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/design/objectTypes/99/exists", body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_type_has_design(99) is False


async def test_object_type_has_design_by_guid_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/design/objectTypes/byGuid/{_ENC}/exists",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_type_has_design_by_guid(_GUID) is True


# --- visibility ---


async def test_visibility_object_type_ids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/visibility/objectTypes/ids", body=[10, 20])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.visibility_object_type_ids()

    assert ids == [10, 20]
    assert all(isinstance(i, int) for i in ids)


async def test_visibility_object_type_ids_empty_when_null(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/visibility/objectTypes/ids", body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.visibility_object_type_ids() == []


async def test_visibility_object_type_guids_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/visibility/objectTypes/guids", body=[_GUID])
    async with IPSClient(config=token_config) as ips:
        assert await ips.visibility_object_type_guids() == [_GUID]


async def test_object_type_has_visibility_attribute_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/visibility/objectTypes/42/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_type_has_visibility_attribute(42) is True


async def test_object_type_has_visibility_attribute_false_when_null(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/visibility/objectTypes/99/exists", body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_type_has_visibility_attribute(99) is False


async def test_object_type_has_visibility_attribute_by_guid_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/visibility/objectTypes/byGuid/{_ENC}/exists",
        body=False,
    )
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_type_has_visibility_attribute_by_guid(_GUID) is False


# --- pdm ---


async def test_pdm_object_type_is_configurable_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/pdm/objectTypes/42/isConfigurable", body=True)
    async with IPSClient(config=token_config) as ips:
        assert await ips.pdm_object_type_is_configurable(42) is True


async def test_pdm_object_type_is_configurable_false_when_null(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/pdm/objectTypes/99/isConfigurable", body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.pdm_object_type_is_configurable(99) is False


async def test_pdm_object_type_is_contextable_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/pdm/objectTypes/42/isContextable", body=True)
    async with IPSClient(config=token_config) as ips:
        assert await ips.pdm_object_type_is_contextable(42) is True


async def test_pdm_object_type_is_root_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/pdm/objectTypes/42/isRoot", body=True)
    async with IPSClient(config=token_config) as ips:
        assert await ips.pdm_object_type_is_root(42) is True


async def test_pdm_relation_type_is_configurable_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/pdm/relationTypes/7/isConfigurable", body=True)
    async with IPSClient(config=token_config) as ips:
        assert await ips.pdm_relation_type_is_configurable(7) is True


async def test_pdm_relation_type_is_partially_configurable_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/pdm/relationTypes/7/isPartiallyConfigurable", body=True)
    async with IPSClient(config=token_config) as ips:
        assert await ips.pdm_relation_type_is_partially_configurable(7) is True


async def test_pdm_relation_type_is_partially_configurable_false_when_null(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/pdm/relationTypes/7/isPartiallyConfigurable", body=None)
    async with IPSClient(config=token_config) as ips:
        assert await ips.pdm_relation_type_is_partially_configurable(7) is False
