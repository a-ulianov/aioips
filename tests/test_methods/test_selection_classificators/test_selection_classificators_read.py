"""Тесты методов чтения раздела классификаторов выбора."""

from uuid import UUID

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_ATTRIBUTE_VALUES = {
    "attributeId": 1029,
    "attributeName": "Архив",
    "attributeGuid": "cad001c5-306c-11d8-b4e9-00304f19f545",
    "attributeAlias": "archive",
    "attributeType": "ftObjectLink",
    "values": [102550, 102551],
}


async def test_classifiers_for_object_type_returns_ints(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/selectionClassificators/byObjectTypeId/1100",
        body=[204, 205, 206],
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.classifiers_for_object_type(1100)

    assert result == [204, 205, 206]
    assert all(isinstance(item, int) for item in result)


async def test_classifiers_for_object_type_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/selectionClassificators/byObjectTypeId/1100",
        body=[],
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.classifiers_for_object_type(1100)

    assert result == []


async def test_classificator_attributes_returns_attribute_values(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/selectionClassificators/204/objects/102550/attributeValues",
        body=[_ATTRIBUTE_VALUES],
    )
    async with IPSClient(config=token_config) as ips:
        attrs = await ips.classificator_attributes(204, 102550)

    assert len(attrs) == 1
    attr = attrs[0]
    assert attr.attribute_id == 1029
    assert attr.attribute_name == "Архив"
    assert attr.attribute_guid == UUID("cad001c5-306c-11d8-b4e9-00304f19f545")
    assert attr.attribute_alias == "archive"
    assert attr.attribute_type == "ftObjectLink"
    assert attr.values == [102550, 102551]


async def test_classificator_attributes_empty_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/selectionClassificators/204/objects/102550/attributeValues",
        body=[],
    )
    async with IPSClient(config=token_config) as ips:
        attrs = await ips.classificator_attributes(204, 102550)

    assert attrs == []


async def test_is_multi_select_classifier_true(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/selectionClassificators/isMultiSelectClassifier",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.is_multi_select_classifier()

    assert result is True


async def test_is_multi_select_classifier_false(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/selectionClassificators/isMultiSelectClassifier",
        body=False,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.is_multi_select_classifier()

    assert result is False


async def test_is_multi_select_classifier_none_is_false(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/selectionClassificators/isMultiSelectClassifier",
        body=None,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.is_multi_select_classifier()

    assert result is False
