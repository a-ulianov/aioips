"""Тесты методов чтения атрибутов объекта."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_ATTR = {
    "name": "Обозначение",
    "attributeID": 12,
    "dbObjectID": 102550,
    "dB_ID": 700,
    "isNull": False,
    "asString": "550.07.305",
    "valuesCount": 1,
    "dataType": "String",
    "isSystem": False,
    "values": ["550.07.305"],
    "descriptions": ["обозначение детали"],
    "readOnly": False,
    "visible": True,
}
_ATTR_VALUES = {
    "attributeId": 12,
    "attributeName": "Обозначение",
    "attributeGuid": "cad00021-306c-11d8-b4e9-00304f19f545",
    "attributeType": "String",
    "values": ["550.07.305"],
    "multipleValued": "single",
    "readOnly": False,
}


async def test_object_attributes(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/objects/102550/attributes", body=[_ATTR])
    async with IPSClient(config=token_config) as ips:
        attributes = await ips.object_attributes(102550)

    assert len(attributes) == 1
    attr = attributes[0]
    assert attr.attribute_id == 12
    assert attr.db_object_id == 102550
    assert attr.db_id == 700
    assert attr.name == "Обозначение"
    assert attr.as_string == "550.07.305"
    assert attr.values == ["550.07.305"]


async def test_object_attribute_unwraps(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/objects/102550/attributes/12",
        body={"entity": _ATTR, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        attr = await ips.object_attribute(102550, 12)

    assert attr is not None
    assert attr.attribute_id == 12


async def test_object_attribute_absent_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/objects/102550/attributes/999",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        attr = await ips.object_attribute(102550, 999)

    assert attr is None


async def test_object_attribute_values(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/objects/102550/attributes/12/values",
        body={"entity": ["550.07.305", "alt"], "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        values = await ips.object_attribute_values(102550, 12)

    assert values == ["550.07.305", "alt"]


async def test_object_attribute_values_absent(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/objects/102550/attributes/12/values",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        values = await ips.object_attribute_values(102550, 12)

    assert values is None


async def test_object_attributes_values(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/objects/102550/attributesValues", body=[_ATTR_VALUES])
    async with IPSClient(config=token_config) as ips:
        values = await ips.object_attributes_values(102550)

    assert len(values) == 1
    item = values[0]
    assert item.attribute_id == 12
    assert item.attribute_name == "Обозначение"
    assert str(item.attribute_guid) == "cad00021-306c-11d8-b4e9-00304f19f545"
    assert item.values == ["550.07.305"]


async def test_attribute_values_null_lists_become_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    # IPS отдаёт null вместо [] — регрессия: должно коэрситься в пустой список.
    fake_ips.add(
        "get",
        "/core/api/objects/4/attributesValues",
        body=[
            {
                "attributeId": 3,
                "attributeType": "ftString",
                "values": ["your-login"],
                "extractedValues": ["your-login"],
                "descriptions": None,
                "multipleValued": "singleValue",
                "computeMode": "notComputableValue",
            }
        ],
    )
    async with IPSClient(config=token_config) as ips:
        values = await ips.object_attributes_values(4)

    assert values[0].descriptions == []
    assert values[0].values == ["your-login"]
