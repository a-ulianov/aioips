"""Тесты дополнительных методов чтения связей и описаний/исходных значений атрибутов."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_RELATION = {
    "relationID": 700123,
    "projID": 102550,
    "partID": 700321,
    "relationType": 3,
    "partObjectID": 102777,
    "guid": "cad00021-306c-11d8-b4e9-00304f19f545",
    "readOnly": False,
}
_ATTR_VALUES = {
    "attributeId": 12,
    "attributeName": "Позиция",
    "attributeType": "String",
    "values": ["5"],
    "extractedValues": ["5"],
    "descriptions": None,
    "multipleValued": "single",
    "computeMode": "notComputableValue",
}


async def test_relation_by_guid_and_project_unwraps(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/byGuid/cad00021-306c-11d8-b4e9-00304f19f545/projects/102550",
        body={"entity": _RELATION, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        relation = await ips.relation_by_guid_and_project(
            "cad00021-306c-11d8-b4e9-00304f19f545", 102550
        )

    assert relation is not None
    assert relation.relation_id == 700123
    assert relation.proj_id == 102550
    assert relation.part_id == 700321


async def test_relation_by_guid_and_project_absent(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/byGuid/00000000-0000-0000-0000-000000000000/projects/102550",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        relation = await ips.relation_by_guid_and_project(
            "00000000-0000-0000-0000-000000000000", 102550
        )

    assert relation is None


async def test_relation_by_project_and_part_unwraps(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/projects/102550/parts/700321",
        body={"entity": _RELATION, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        relation = await ips.relation_by_project_and_part(102550, 700321)

    assert relation is not None
    assert relation.relation_type == 3
    assert relation.part_object_id == 102777


async def test_relation_by_project_and_part_absent(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/projects/102550/parts/999",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        relation = await ips.relation_by_project_and_part(102550, 999)

    assert relation is None


async def test_relation_attribute_descriptions_unwraps(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/700123/attributes/12/descriptions",
        body={"entity": ["позиция в составе", "доп."], "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        descriptions = await ips.relation_attribute_descriptions(700123, 12)

    assert descriptions == ["позиция в составе", "доп."]


async def test_relation_attribute_descriptions_absent(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/700123/attributes/999/descriptions",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        descriptions = await ips.relation_attribute_descriptions(700123, 999)

    assert descriptions is None


async def test_relation_attributes_descriptions_unwraps(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/700123/attributesDescriptions",
        body={
            "entity": [{"attributeId": 12, "descriptions": ["позиция"]}],
            "isEntityPresent": True,
        },
    )
    async with IPSClient(config=token_config) as ips:
        items = await ips.relation_attributes_descriptions(700123)

    assert items is not None
    assert items[0]["attributeId"] == 12
    assert items[0]["descriptions"] == ["позиция"]


async def test_relation_attributes_descriptions_absent(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/700123/attributesDescriptions",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        items = await ips.relation_attributes_descriptions(700123)

    assert items is None


async def test_relation_attributes_init_values(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/700123/attributesInitValues",
        body=[_ATTR_VALUES],
    )
    async with IPSClient(config=token_config) as ips:
        init = await ips.relation_attributes_init_values(700123)

    assert len(init) == 1
    item = init[0]
    assert item.attribute_id == 12
    assert item.values == ["5"]
    # IPS отдаёт null вместо [] — должно коэрситься в пустой список.
    assert item.descriptions == []


async def test_relation_attributes_init_values_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/relations/700123/attributesInitValues",
        body=[],
    )
    async with IPSClient(config=token_config) as ips:
        init = await ips.relation_attributes_init_values(700123)

    assert init == []
