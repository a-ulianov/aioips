"""Тесты методов чтения типов атрибутов раздела metadata."""

from urllib.parse import quote
from uuid import UUID

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.common.enumerations import ComputeValueMode, FieldType, MultiValueMode

_GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"

_ATTRIBUTE_TYPE = {
    "id": 1029,
    "guid": _GUID,
    "name": "Архив",
    "shortName": "Арх",
    "fieldType": "ftObjectLink",
    "realFieldType": "ftUnknown",
    "multiValueMode": "singleValue",
    "computed": "notComputableValue",
    "isContent": False,
    "options": None,
    "masterAttributeId": 0,
    "sourceAttributeId": 0,
    "possibleValues": None,
}

_ATTRIBUTE_FOR_OBJECT_TYPE = {
    "attributeId": 1029,
    "objectTypeId": 1742,
    "computed": "notComputableValue",
    "required": "auto",
    "public": "public",
    "isContent": False,
    "options": None,
    "fieldType": "ftObjectLink",
    "validationRule": "",
}


async def test_attribute_types_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeTypes",
        body=[_ATTRIBUTE_TYPE, _ATTRIBUTE_TYPE],
    )
    async with IPSClient(config=token_config) as ips:
        types = await ips.attribute_types()

    assert len(types) == 2
    first = types[0]
    assert first.id == 1029
    assert first.name == "Архив"
    assert first.field_type == FieldType.OBJECT_LINK
    assert first.multi_value_mode == MultiValueMode.SINGLE_VALUE
    assert first.computed == ComputeValueMode.NOT_COMPUTABLE
    # options пришёл null — должен стать пустым списком
    assert first.options == []
    assert first.guid == UUID(_GUID)


async def test_attribute_type_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeTypes/1029",
        body={"entity": _ATTRIBUTE_TYPE, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        attr = await ips.attribute_type(1029)

    assert attr is not None
    assert attr.id == 1029
    assert attr.field_type == FieldType.OBJECT_LINK
    assert attr.master_attribute_id == 0


async def test_attribute_type_returns_none_when_absent(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeTypes/999",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        attr = await ips.attribute_type(999)

    assert attr is None


async def test_attribute_type_by_guid_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/attributeTypes/byGuid/{_GUID}",
        body={"entity": _ATTRIBUTE_TYPE, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        attr = await ips.attribute_type_by_guid(_GUID)

    assert attr is not None
    assert attr.guid == UUID(_GUID)
    assert attr.name == "Архив"


async def test_attribute_type_by_guid_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        f"/core/api/metadata/attributeTypes/byGuid/{_GUID}",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        attr = await ips.attribute_type_by_guid(_GUID)

    assert attr is None


async def test_attribute_type_id_by_name_returns_int(token_config: IPSConfig, fake_ips: FakeIPS):
    # Имя кодируется в URL, но aiohttp на сервере отдаёт уже декодированный path,
    # поэтому мок регистрируем по исходному (декодированному) пути.
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeTypes/byName/Архив/id",
        body=1029,
    )
    async with IPSClient(config=token_config) as ips:
        attr_id = await ips.attribute_type_id_by_name("Архив")

    assert attr_id == 1029
    assert isinstance(attr_id, int)


async def test_attribute_type_id_by_name_encodes_name(token_config: IPSConfig, fake_ips: FakeIPS):
    # Проверяем, что имя с пробелом кодируется в URL (пробел → %20, не "+").
    name = "Номер документа"
    assert "%20" in quote(name, safe="")  # пробел кодируется как %20, а не "+"
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeTypes/byName/Номер документа/id",
        body=42,
    )
    async with IPSClient(config=token_config) as ips:
        attr_id = await ips.attribute_type_id_by_name(name)

    assert attr_id == 42


async def test_attributes_for_object_type_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeForObjectTypeList/1742",
        body=[_ATTRIBUTE_FOR_OBJECT_TYPE, _ATTRIBUTE_FOR_OBJECT_TYPE],
    )
    async with IPSClient(config=token_config) as ips:
        attrs = await ips.attribute_for_object_type_list(1742)

    assert len(attrs) == 2
    first = attrs[0]
    assert first.attribute_id == 1029
    assert first.object_type_id == 1742
    assert first.field_type == FieldType.OBJECT_LINK
    assert first.required == "auto"
    assert first.options == []
