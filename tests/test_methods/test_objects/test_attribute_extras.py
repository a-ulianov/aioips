"""Тесты дополнительных методов чтения атрибутов объекта.

Покрывают описания атрибутов, строковое представление значения и начальные
(инициализирующие) значения. Для методов с result-обёрткой проверяются оба
случая: присутствующая сущность (``entity``) и её отсутствие (``None``).
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig


async def test_object_attributes_descriptions_unwraps(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/objects/102550/attributesDescriptions",
        body={
            "entity": [
                {"attributeId": 12, "descriptions": ["обозначение детали"]},
                {"attributeId": 13, "descriptions": None},
            ],
            "isEntityPresent": True,
        },
    )
    async with IPSClient(config=token_config) as ips:
        items = await ips.object_attributes_descriptions(102550)

    assert items is not None
    assert len(items) == 2
    assert items[0]["attributeId"] == 12
    assert items[0]["descriptions"] == ["обозначение детали"]


async def test_object_attributes_descriptions_absent_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/objects/102550/attributesDescriptions",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        items = await ips.object_attributes_descriptions(102550)

    assert items is None


async def test_object_attribute_descriptions_unwraps(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/objects/102550/attributes/12/descriptions",
        body={"entity": ["обозначение детали", "альт"], "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        descriptions = await ips.object_attribute_descriptions(102550, 12)

    assert descriptions == ["обозначение детали", "альт"]


async def test_object_attribute_descriptions_absent_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/objects/102550/attributes/999/descriptions",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        descriptions = await ips.object_attribute_descriptions(102550, 999)

    assert descriptions is None


async def test_object_attribute_as_string_returns_string(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "post",
        "/core/api/objects/102550/attributes/12/asString",
        body="550.07.305",
    )
    async with IPSClient(config=token_config) as ips:
        text = await ips.object_attribute_as_string(102550, 12)

    assert text == "550.07.305"
    captured = fake_ips.requests[-1]
    assert captured.method == "POST"
    assert captured.body == {}


async def test_object_attribute_as_string_non_string_returns_none(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "post",
        "/core/api/objects/102550/attributes/12/asString",
        body=None,
    )
    async with IPSClient(config=token_config) as ips:
        text = await ips.object_attribute_as_string(102550, 12)

    assert text is None


async def test_object_attributes_init_values(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/objects/102550/attributesInitValues",
        body=[
            {
                "attributeId": 12,
                "attributeName": "Обозначение",
                "attributeType": "ftString",
                "values": ["000.00.000"],
                "descriptions": None,
                "multipleValued": "singleValue",
                "computeMode": "notComputableValue",
            }
        ],
    )
    async with IPSClient(config=token_config) as ips:
        init = await ips.object_attributes_init_values(102550, attr_ids=[12])

    assert len(init) == 1
    item = init[0]
    assert item.attribute_id == 12
    assert item.values == ["000.00.000"]
    # IPS отдаёт null вместо [] — должно коэрситься в пустой список.
    assert item.descriptions == []
