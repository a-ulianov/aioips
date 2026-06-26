"""Тесты методов «атрибут для типа объекта/связи» раздела metadata."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.common.enumerations import ComputeValueMode, FieldType

_OBJECT_TYPE_GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"
_RELATION_TYPE_GUID = "22222222-2222-2222-2222-222222222222"
_ATTRIBUTE_TYPE_GUID = "33333333-3333-3333-3333-333333333333"

# Полный набор ключей DTO ImsAttributeForRelationTypeDto (из swagger). casing — точно
# как в JSON ответа сервера, чтобы тест ловил расхождения алиасов snake↔camel.
_ATTRIBUTE_FOR_RELATION_TYPE = {
    "attributeId": 1029,
    "computed": "notComputableValue",
    "formula": None,
    "languageId": None,
    "areaId": None,
    "optimizationMode": "notFound",
    "required": "auto",
    "isContent": False,
    "options": None,
    "masterAttributeId": 0,
    "sourceAttributeId": 0,
    "validationRule": "",
    "mask": None,
    "defaultValue": None,
    "relationTypeId": 500,
    "fieldType": "ftObjectLink",
    "realFieldType": "ftUnknown",
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

_ATTRIBUTE_TYPE = {
    "id": 1029,
    "guid": _ATTRIBUTE_TYPE_GUID,
    "name": "Архив",
    "fieldType": "ftObjectLink",
    "computed": "notComputableValue",
    "options": None,
    "possibleValues": None,
}


# --- attribute for object type (single, by ids) ---------------------------------


async def test_attribute_for_object_type_unwraps_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeForObjectType/1742/1029",
        body={"entity": _ATTRIBUTE_FOR_OBJECT_TYPE, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        binding = await ips.attribute_for_object_type(1742, 1029)

    assert binding is not None
    assert binding.attribute_id == 1029
    assert binding.object_type_id == 1742
    assert binding.field_type == FieldType.OBJECT_LINK
    assert binding.options == []


async def test_attribute_for_object_type_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeForObjectType/1742/999",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        binding = await ips.attribute_for_object_type(1742, 999)

    assert binding is None


async def test_attribute_for_object_type_by_guids_unwraps_entity(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/attributeForObjectType/byGuid/{_OBJECT_TYPE_GUID}"
        f"/{_ATTRIBUTE_TYPE_GUID}",
        body={"entity": _ATTRIBUTE_FOR_OBJECT_TYPE, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        binding = await ips.attribute_for_object_type_by_guids(
            _OBJECT_TYPE_GUID, _ATTRIBUTE_TYPE_GUID
        )

    assert binding is not None
    assert binding.attribute_id == 1029


async def test_attributes_for_object_type_by_guid_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/attributeForObjectTypeList/byGuid/{_OBJECT_TYPE_GUID}",
        body=[_ATTRIBUTE_FOR_OBJECT_TYPE, _ATTRIBUTE_FOR_OBJECT_TYPE],
    )
    async with IPSClient(config=token_config) as ips:
        attrs = await ips.attribute_for_object_type_list_by_guid(_OBJECT_TYPE_GUID)

    assert len(attrs) == 2
    assert attrs[0].object_type_id == 1742


async def test_all_attributes_for_object_type_list_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/allAttributesForObjectTypeList/1029",
        body=[_ATTRIBUTE_FOR_OBJECT_TYPE],
    )
    async with IPSClient(config=token_config) as ips:
        bindings = await ips.all_attributes_for_object_type_list(1029)

    assert len(bindings) == 1
    assert bindings[0].attribute_id == 1029


async def test_all_attributes_for_object_type_list_by_guid_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/allAttributesForObjectTypeList/byGuid/{_ATTRIBUTE_TYPE_GUID}",
        body=[_ATTRIBUTE_FOR_OBJECT_TYPE],
    )
    async with IPSClient(config=token_config) as ips:
        bindings = await ips.all_attributes_for_object_type_list_by_guid(_ATTRIBUTE_TYPE_GUID)

    assert len(bindings) == 1
    assert bindings[0].object_type_id == 1742


# --- attribute for relation type ------------------------------------------------


async def test_attribute_for_relation_type_unwraps_entity(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeForRelationType/500/1029",
        body={"entity": _ATTRIBUTE_FOR_RELATION_TYPE, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        binding = await ips.attribute_for_relation_type(500, 1029)

    assert binding is not None
    # Проверяем разбор всех значимых ключей DTO (alias snake↔camel из swagger).
    assert binding.attribute_id == 1029
    assert binding.relation_type_id == 500
    assert binding.computed == ComputeValueMode.NOT_COMPUTABLE
    assert binding.required == "auto"
    assert binding.is_content is False
    assert binding.master_attribute_id == 0
    assert binding.source_attribute_id == 0
    assert binding.optimization_mode == "notFound"
    assert binding.validation_rule == ""
    assert binding.field_type == FieldType.OBJECT_LINK
    assert binding.real_field_type == FieldType.UNKNOWN
    # options пришёл null — должен стать пустым списком
    assert binding.options == []


async def test_attribute_for_relation_type_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeForRelationType/500/999",
        body={"entity": None, "isEntityPresent": False},
    )
    async with IPSClient(config=token_config) as ips:
        binding = await ips.attribute_for_relation_type(500, 999)

    assert binding is None


async def test_attribute_for_relation_type_by_guids_unwraps_entity(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/attributeForRelationType/byGuid/{_RELATION_TYPE_GUID}"
        f"/{_ATTRIBUTE_TYPE_GUID}",
        body={"entity": _ATTRIBUTE_FOR_RELATION_TYPE, "isEntityPresent": True},
    )
    async with IPSClient(config=token_config) as ips:
        binding = await ips.attribute_for_relation_type_by_guids(
            _RELATION_TYPE_GUID, _ATTRIBUTE_TYPE_GUID
        )

    assert binding is not None
    assert binding.relation_type_id == 500


async def test_attributes_for_relation_type_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeForRelationTypeList/500",
        body=[_ATTRIBUTE_FOR_RELATION_TYPE, _ATTRIBUTE_FOR_RELATION_TYPE],
    )
    async with IPSClient(config=token_config) as ips:
        attrs = await ips.attribute_for_relation_type_list(500)

    assert len(attrs) == 2
    assert attrs[0].attribute_id == 1029
    assert attrs[0].relation_type_id == 500


async def test_attributes_for_relation_type_by_guid_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/attributeForRelationTypeList/byGuid/{_RELATION_TYPE_GUID}",
        body=[_ATTRIBUTE_FOR_RELATION_TYPE],
    )
    async with IPSClient(config=token_config) as ips:
        attrs = await ips.attribute_for_relation_type_list_by_guid(_RELATION_TYPE_GUID)

    assert len(attrs) == 1
    assert attrs[0].relation_type_id == 500


async def test_all_attributes_for_relation_type_list_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        "/core/api/metadata/allAttributesForRelationTypeList/1029",
        body=[_ATTRIBUTE_FOR_RELATION_TYPE],
    )
    async with IPSClient(config=token_config) as ips:
        bindings = await ips.all_attributes_for_relation_type_list(1029)

    assert len(bindings) == 1
    assert bindings[0].relation_type_id == 500


async def test_all_attributes_for_relation_type_list_by_guid_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/allAttributesForRelationTypeList/byGuid/{_ATTRIBUTE_TYPE_GUID}",
        body=[_ATTRIBUTE_FOR_RELATION_TYPE],
    )
    async with IPSClient(config=token_config) as ips:
        bindings = await ips.all_attributes_for_relation_type_list_by_guid(_ATTRIBUTE_TYPE_GUID)

    assert len(bindings) == 1
    assert bindings[0].attribute_id == 1029


# --- used sorted / unsorted attributes ------------------------------------------


async def test_used_sorted_attributes_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/usedSortedAttributes",
        body=[_ATTRIBUTE_TYPE, _ATTRIBUTE_TYPE],
    )
    async with IPSClient(config=token_config) as ips:
        attrs = await ips.used_sorted_attributes()

    assert len(attrs) == 2
    assert attrs[0].id == 1029
    assert attrs[0].field_type == FieldType.OBJECT_LINK


async def test_used_sorted_attribute_ids_returns_ints(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/usedSortedAttributes/ids",
        body=[1029, 1, 42],
    )
    async with IPSClient(config=token_config) as ips:
        ids = await ips.used_sorted_attribute_ids()

    assert ids == [1029, 1, 42]
    assert all(isinstance(i, int) for i in ids)


async def test_used_unsorted_attribute_ids_returns_ints(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "get",
        "/core/api/metadata/usedUnsortedAttributes/ids",
        body=[1029, 1, 42],
    )
    async with IPSClient(config=token_config) as ips:
        ids = await ips.used_unsorted_attribute_ids()

    assert set(ids) == {1029, 1, 42}
