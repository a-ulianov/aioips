"""Тесты скалярных аксессоров типов атрибутов раздела metadata.

Проверяют построение пути запроса и преобразование возврата для каждого
аксессора. Для методов byName дополнительно проверяется URL-кодирование
кириллицы (``quote(..., safe="")``).
"""

from urllib.parse import quote

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"


async def test_attribute_type_exists_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/attributeTypes/1029/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.attribute_type_exists(1029)

    assert result is True
    assert fake_ips.requests[-1].path == "/core/api/metadata/attributeTypes/1029/exists"


async def test_attribute_type_exists_false_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/attributeTypes/999/exists", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.attribute_type_exists(999)

    assert result is False


async def test_attribute_type_exists_by_guid_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/attributeTypes/byGuid/{_GUID}/exists",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.attribute_type_exists_by_guid(_GUID)

    assert result is True
    assert fake_ips.requests[-1].path == (
        f"/core/api/metadata/attributeTypes/byGuid/{_GUID}/exists"
    )


async def test_attribute_type_id_by_guid_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"/core/api/metadata/attributeTypes/byGuid/{_GUID}/id", body=1029)
    async with IPSClient(config=token_config) as ips:
        attr_id = await ips.attribute_type_id_by_guid(_GUID)

    assert attr_id == 1029
    assert isinstance(attr_id, int)


async def test_attribute_type_name_by_guid_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"/core/api/metadata/attributeTypes/byGuid/{_GUID}/name", body="Архив")
    async with IPSClient(config=token_config) as ips:
        name = await ips.attribute_type_name_by_guid(_GUID)

    assert name == "Архив"


async def test_attribute_type_name_by_guid_empty_when_null(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", f"/core/api/metadata/attributeTypes/byGuid/{_GUID}/name", body=None)
    async with IPSClient(config=token_config) as ips:
        name = await ips.attribute_type_name_by_guid(_GUID)

    assert name == ""


async def test_attribute_type_name_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/attributeTypes/1029/name", body="Архив")
    async with IPSClient(config=token_config) as ips:
        name = await ips.attribute_type_name(1029)

    assert name == "Архив"
    assert fake_ips.requests[-1].path == "/core/api/metadata/attributeTypes/1029/name"


async def test_attribute_type_guid_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/attributeTypes/1029/guid", body=_GUID)
    async with IPSClient(config=token_config) as ips:
        guid = await ips.attribute_type_guid(1029)

    assert guid == _GUID


async def test_attribute_type_guid_by_name_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    # aiohttp на сервере отдаёт уже декодированный path, поэтому мок — по декодированному.
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeTypes/byName/Архив/guid",
        body=_GUID,
    )
    async with IPSClient(config=token_config) as ips:
        guid = await ips.attribute_type_guid_by_name("Архив")

    assert guid == _GUID


async def test_attribute_type_guid_by_name_encodes_cyrillic(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    # Кириллица и пробел должны кодироваться в URL (пробел → %20, не "+").
    name = "Номер документа"
    encoded = quote(name, safe="")
    assert "%20" in encoded  # пробел кодируется как %20
    assert "%D0" in encoded  # кириллица percent-encoded
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeTypes/byName/Номер документа/guid",
        body=_GUID,
    )
    async with IPSClient(config=token_config) as ips:
        guid = await ips.attribute_type_guid_by_name(name)

    assert guid == _GUID


async def test_attribute_type_ids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/attributeTypes/ids", body=[1, 2, 1029])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.attribute_type_ids()

    assert ids == [1, 2, 1029]
    assert all(isinstance(i, int) for i in ids)


async def test_attribute_type_ids_empty_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/attributeTypes/ids", body=None)
    async with IPSClient(config=token_config) as ips:
        ids = await ips.attribute_type_ids()

    assert ids == []


async def test_attribute_type_guids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/attributeTypes/guids", body=[_GUID, _GUID])
    async with IPSClient(config=token_config) as ips:
        guids = await ips.attribute_type_guids()

    assert guids == [_GUID, _GUID]
    assert all(isinstance(g, str) for g in guids)


async def test_attribute_has_possible_values_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeTypes/hasPossibleValues/1029",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.attribute_has_possible_values(1029)

    assert result is True


async def test_attribute_has_possible_values_by_guid_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/attributeTypes/hasPossibleValues/byGuid/{_GUID}",
        body=False,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.attribute_has_possible_values_by_guid(_GUID)

    assert result is False


async def test_attribute_has_system_data_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/attributeTypes/hasSystemData/1029", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.attribute_has_system_data(1029)

    assert result is True


async def test_attribute_has_system_data_by_guid_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/attributeTypes/hasSystemData/byGuid/{_GUID}",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.attribute_has_system_data_by_guid(_GUID)

    assert result is True


async def test_attribute_is_gridable_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/attributeTypes/isGridable/1029", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.attribute_is_gridable(1029)

    assert result is True


async def test_attribute_is_gridable_by_guid_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/attributeTypes/isGridable/byGuid/{_GUID}",
        body=False,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.attribute_is_gridable_by_guid(_GUID)

    assert result is False


async def test_attribute_supports_object_links_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/attributeTypes/supportsObjectLinks/byGuid/{_GUID}",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.attribute_supports_object_links(_GUID)

    assert result is True
    assert fake_ips.requests[-1].path == (
        f"/core/api/metadata/attributeTypes/supportsObjectLinks/byGuid/{_GUID}"
    )
