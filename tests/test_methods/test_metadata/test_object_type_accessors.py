"""Тесты скалярных аксессоров типов объектов раздела metadata."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_TYPE_GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"
# GUID с символами, требующими кодирования в URL (для проверки quote).
_GUID_NEEDS_QUOTE = "a b/c"


async def test_object_type_exists_true(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/objectTypes/1742/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_type_exists(1742)

    assert result is True


async def test_object_type_exists_false_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/objectTypes/999/exists", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_type_exists(999)

    assert result is False


async def test_object_type_exists_by_guid_true(token_config: IPSConfig, fake_ips: FakeIPS):
    # FakeIPS получает уже декодированный путь, поэтому мок регистрируем по исходному GUID.
    fake_ips.add(
        "get",
        f"/core/api/metadata/objectTypes/byGuid/{_TYPE_GUID}/exists",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_type_exists_by_guid(_TYPE_GUID)

    assert result is True


async def test_object_type_exists_by_guid_encodes_guid(token_config: IPSConfig, fake_ips: FakeIPS):
    # Декодированный путь содержит пробел и слэш — значит quote(safe="") отработал.
    fake_ips.add(
        "get",
        f"/core/api/metadata/objectTypes/byGuid/{_GUID_NEEDS_QUOTE}/exists",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_type_exists_by_guid(_GUID_NEEDS_QUOTE)

    assert result is True


async def test_object_type_id_by_guid_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/objectTypes/byGuid/{_TYPE_GUID}/id",
        body=1742,
    )
    async with IPSClient(config=token_config) as ips:
        type_id = await ips.object_type_id_by_guid(_TYPE_GUID)

    assert type_id == 1742
    assert isinstance(type_id, int)


async def test_object_type_name_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/objectTypes/1742/name", body="Document")
    async with IPSClient(config=token_config) as ips:
        name = await ips.object_type_name(1742)

    assert name == "Document"


async def test_object_type_name_empty_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/objectTypes/999/name", body=None)
    async with IPSClient(config=token_config) as ips:
        name = await ips.object_type_name(999)

    assert name == ""


async def test_object_type_name_by_guid_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/objectTypes/byGuid/{_TYPE_GUID}/name",
        body="Document",
    )
    async with IPSClient(config=token_config) as ips:
        name = await ips.object_type_name_by_guid(_TYPE_GUID)

    assert name == "Document"


async def test_object_type_guid_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/objectTypes/1742/guid", body=_TYPE_GUID)
    async with IPSClient(config=token_config) as ips:
        guid = await ips.object_type_guid(1742)

    assert guid == _TYPE_GUID


async def test_object_type_full_name_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/objectTypes/1742/fullName",
        body="Объекты\\Документы\\Документ",
    )
    async with IPSClient(config=token_config) as ips:
        full_name = await ips.object_type_full_name(1742)

    assert full_name == "Объекты\\Документы\\Документ"


async def test_object_type_object_name_returns_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/objectTypes/1742/objectName", body="Документ")
    async with IPSClient(config=token_config) as ips:
        name = await ips.object_type_object_name(1742)

    assert name == "Документ"


async def test_object_type_object_name_by_guid_returns_str(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/objectTypes/byGuid/{_TYPE_GUID}/objectName",
        body="Документ",
    )
    async with IPSClient(config=token_config) as ips:
        name = await ips.object_type_object_name_by_guid(_TYPE_GUID)

    assert name == "Документ"


async def test_object_type_is_local_true(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/objectTypes/1742/isLocal", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_type_is_local(1742)

    assert result is True


async def test_object_type_is_local_false_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/objectTypes/1742/isLocal", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_type_is_local(1742)

    assert result is False


async def test_object_type_is_local_by_guid_true(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/objectTypes/byGuid/{_TYPE_GUID}/isLocal",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_type_is_local_by_guid(_TYPE_GUID)

    assert result is True
