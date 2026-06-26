"""Тесты методов чтения атрибутов СВЯЗИ."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_ATTR = {
    "name": "Позиция",
    "attributeID": 12,
    "dbObjectID": 102550,
    "dB_ID": 700,
    "isNull": False,
    "asString": "5",
    "valuesCount": 1,
    "dataType": "String",
    "isSystem": False,
    "values": ["5"],
    "descriptions": ["позиция в составе"],
    "readOnly": False,
    "visible": True,
}
_ATTR_VALUES = {
    "attributeId": 12,
    "attributeName": "Позиция",
    "attributeGuid": "cad00021-306c-11d8-b4e9-00304f19f545",
    "attributeType": "String",
    "values": ["5"],
    "multipleValued": "single",
    "readOnly": False,
}


async def test_relation_attributes(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/relations/700123/attributes", body=[_ATTR])
    async with IPSClient(config=token_config) as ips:
        attributes = await ips.relation_attributes(700123)

    assert len(attributes) == 1
    attr = attributes[0]
    assert attr.attribute_id == 12
    assert attr.db_object_id == 102550
    assert attr.db_id == 700
    assert attr.name == "Позиция"
    assert attr.as_string == "5"
    assert attr.values == ["5"]


async def test_relation_attribute_unwraps(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/700123/attributes/12",
        body={"entity": _ATTR, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        attr = await ips.relation_attribute(700123, 12)

    assert attr is not None
    assert attr.attribute_id == 12


async def test_relation_attribute_absent_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/700123/attributes/999",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        attr = await ips.relation_attribute(700123, 999)

    assert attr is None


async def test_relation_attribute_values(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/700123/attributes/12/values",
        body={"entity": ["5", "alt"], "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        values = await ips.relation_attribute_values(700123, 12)

    assert values == ["5", "alt"]


async def test_relation_attribute_values_absent(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/700123/attributes/12/values",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        values = await ips.relation_attribute_values(700123, 12)

    assert values is None


async def test_relation_attributes_values(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/relations/700123/attributesValues", body=[_ATTR_VALUES])
    async with IPSClient(config=token_config) as ips:
        values = await ips.relation_attributes_values(700123)

    assert len(values) == 1
    item = values[0]
    assert item.attribute_id == 12
    assert item.attribute_name == "Позиция"
    assert str(item.attribute_guid) == "cad00021-306c-11d8-b4e9-00304f19f545"
    assert item.values == ["5"]


async def test_relation_attributes_values_null_lists_become_empty(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    # IPS отдаёт null вместо [] — регрессия: должно коэрситься в пустой список.
    fake_ips.add(
        "get",
        "/core/api/relations/700123/attributesValues",
        body=[
            {
                "attributeId": 12,
                "attributeType": "ftString",
                "values": ["5"],
                "extractedValues": ["5"],
                "descriptions": None,
                "multipleValued": "singleValue",
                "computeMode": "notComputableValue",
            }
        ],
    )
    async with IPSClient(config=token_config) as ips:
        values = await ips.relation_attributes_values(700123)

    assert values[0].descriptions == []
    assert values[0].values == ["5"]
