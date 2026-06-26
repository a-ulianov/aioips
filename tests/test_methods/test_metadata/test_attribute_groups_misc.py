"""Тесты методов групп атрибутов, применимости и разрозненных справок metadata.

Проверяют построение пути запроса и преобразование возврата для новых методов:
группы атрибутов (схема :class:`AttributeGroup` через unwrap ``entity``), состав
группы (списки int/str), применимость типа атрибута (голый строковый enum
:class:`AttributeTypeApplicability`), булевы предикаты использования, связанные
типы объектов атрибута-ссылки (unwrap ``entity`` → ``list[int] | None``) и
формульные зависимости.

Новые mixin'ы намеренно не подключены к ``MetadataAPI`` (``__init__.py`` не
трогаем по контракту), поэтому здесь собирается локальный композит ``_Client``
из тестируемых mixin'ов поверх ядра :class:`APIManager`.
"""

from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.core import APIManager
from aioips.methods.metadata.attribute_group import AttributeGroupMixin
from aioips.methods.metadata.attribute_group_by_guid import AttributeGroupByGuidMixin
from aioips.methods.metadata.attribute_group_guid import AttributeGroupGuidMixin
from aioips.methods.metadata.attribute_group_id_by_guid import AttributeGroupIdByGuidMixin
from aioips.methods.metadata.attribute_is_in_use import AttributeIsInUseMixin
from aioips.methods.metadata.attribute_is_in_use_by_guid import AttributeIsInUseByGuidMixin
from aioips.methods.metadata.attribute_linked_object_type_ids import (
    AttributeLinkedObjectTypeIdsMixin,
)
from aioips.methods.metadata.attribute_type_applicability import AttributeTypeApplicabilityMixin
from aioips.methods.metadata.attribute_type_applicability_by_guid import (
    AttributeTypeApplicabilityByGuidMixin,
)
from aioips.methods.metadata.attributes_in_group_guids import AttributesInGroupGuidsMixin
from aioips.methods.metadata.attributes_in_group_guids_by_guid import (
    AttributesInGroupGuidsByGuidMixin,
)
from aioips.methods.metadata.attributes_in_group_ids import AttributesInGroupIdsMixin
from aioips.methods.metadata.attributes_in_group_ids_by_guid import (
    AttributesInGroupIdsByGuidMixin,
)
from aioips.methods.metadata.object_link_attribute_type_ids import (
    ObjectLinkAttributeTypeIdsMixin,
)
from aioips.methods.metadata.related_formula_attributes_for_object import (
    RelatedFormulaAttributesForObjectMixin,
)
from aioips.methods.metadata.related_formula_attributes_for_relation import (
    RelatedFormulaAttributesForRelationMixin,
)
from aioips.methods.metadata.relation_type_for_prj_link import RelationTypeForPrjLinkMixin
from aioips.schemas.metadata import AttributeApplicabilityKind

_GUID = "cad001c5-306c-11d8-b4e9-00304f19f545"


class _Client(
    AttributeGroupMixin,
    AttributeGroupByGuidMixin,
    AttributeGroupIdByGuidMixin,
    AttributeGroupGuidMixin,
    AttributesInGroupIdsMixin,
    AttributesInGroupGuidsMixin,
    AttributesInGroupIdsByGuidMixin,
    AttributesInGroupGuidsByGuidMixin,
    AttributeTypeApplicabilityMixin,
    AttributeTypeApplicabilityByGuidMixin,
    AttributeIsInUseMixin,
    AttributeIsInUseByGuidMixin,
    AttributeLinkedObjectTypeIdsMixin,
    ObjectLinkAttributeTypeIdsMixin,
    RelationTypeForPrjLinkMixin,
    RelatedFormulaAttributesForObjectMixin,
    RelatedFormulaAttributesForRelationMixin,
    APIManager,
):
    """Локальный композит тестируемых mixin'ов поверх ядра клиента."""


def _config(fake_ips: FakeIPS) -> IPSConfig:
    return IPSConfig(
        base_url=fake_ips.base_url,
        access_token="test-token",
        retry_min_wait=0.01,
        retry_max_wait=0.02,
        _env_file=None,
    )


_GROUP_BODY = {
    "id": 42,
    "guid": _GUID,
    "name": "Геометрия",
    "note": "примечание",
    "areaId": None,
    "languageId": None,
    "parentId": 0,
}


# --- группа атрибутов: схема ---


async def test_attribute_group_unwraps_entity(fake_ips: FakeIPS) -> None:
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeGroups/42",
        body={"entity": _GROUP_BODY, "isEntityPresent": True},
    )
    async with _Client(config=_config(fake_ips)) as ips:
        group = await ips.attribute_group(42)

    assert group is not None
    # ключи новой схемы AttributeGroup
    assert group.id == 42
    assert group.name == "Геометрия"
    assert group.note == "примечание"
    assert group.parent_id == 0
    assert str(group.guid) == _GUID
    assert fake_ips.requests[-1].path == "/core/api/metadata/attributeGroups/42"


async def test_attribute_group_none_when_absent(fake_ips: FakeIPS) -> None:
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeGroups/99",
        body={"entity": None, "isEntityPresent": False},
    )
    async with _Client(config=_config(fake_ips)) as ips:
        assert await ips.attribute_group(99) is None


async def test_attribute_group_by_guid_unwraps_entity(fake_ips: FakeIPS) -> None:
    fake_ips.add(
        "get",
        f"/core/api/metadata/attributeGroups/byGuid/{_GUID}",
        body={"entity": _GROUP_BODY, "isEntityPresent": True},
    )
    async with _Client(config=_config(fake_ips)) as ips:
        group = await ips.attribute_group_by_guid(_GUID)

    assert group is not None
    assert group.parent_id == 0


# --- группа атрибутов: id/guid мосты ---


async def test_attribute_group_id_by_guid_returns_int(fake_ips: FakeIPS) -> None:
    fake_ips.add("get", f"/core/api/metadata/attributeGroups/byGuid/{_GUID}/id", body=42)
    async with _Client(config=_config(fake_ips)) as ips:
        result = await ips.attribute_group_id_by_guid(_GUID)

    assert result == 42
    assert isinstance(result, int)


async def test_attribute_group_guid_returns_str(fake_ips: FakeIPS) -> None:
    fake_ips.add("get", "/core/api/metadata/attributeGroups/42/guid", body=_GUID)
    async with _Client(config=_config(fake_ips)) as ips:
        assert await ips.attribute_group_guid(42) == _GUID


async def test_attribute_group_guid_empty_when_null(fake_ips: FakeIPS) -> None:
    fake_ips.add("get", "/core/api/metadata/attributeGroups/42/guid", body=None)
    async with _Client(config=_config(fake_ips)) as ips:
        assert await ips.attribute_group_guid(42) == ""


# --- состав группы ---


async def test_attributes_in_group_ids_returns_list(fake_ips: FakeIPS) -> None:
    fake_ips.add("get", "/core/api/metadata/attributesInGroup/42/ids", body=[1, 2, 3])
    async with _Client(config=_config(fake_ips)) as ips:
        ids = await ips.attributes_in_group_ids(42)

    assert ids == [1, 2, 3]
    assert all(isinstance(i, int) for i in ids)


async def test_attributes_in_group_ids_empty_when_null(fake_ips: FakeIPS) -> None:
    fake_ips.add("get", "/core/api/metadata/attributesInGroup/42/ids", body=None)
    async with _Client(config=_config(fake_ips)) as ips:
        assert await ips.attributes_in_group_ids(42) == []


async def test_attributes_in_group_guids_returns_list(fake_ips: FakeIPS) -> None:
    fake_ips.add("get", "/core/api/metadata/attributesInGroup/42/guids", body=[_GUID])
    async with _Client(config=_config(fake_ips)) as ips:
        assert await ips.attributes_in_group_guids(42) == [_GUID]


async def test_attributes_in_group_ids_by_guid_returns_list(fake_ips: FakeIPS) -> None:
    fake_ips.add("get", f"/core/api/metadata/attributesInGroup/byGuid/{_GUID}/ids", body=[5, 6])
    async with _Client(config=_config(fake_ips)) as ips:
        assert await ips.attributes_in_group_ids_by_guid(_GUID) == [5, 6]


async def test_attributes_in_group_guids_by_guid_returns_list(fake_ips: FakeIPS) -> None:
    fake_ips.add("get", f"/core/api/metadata/attributesInGroup/byGuid/{_GUID}/guids", body=[_GUID])
    async with _Client(config=_config(fake_ips)) as ips:
        assert await ips.attributes_in_group_guids_by_guid(_GUID) == [_GUID]


# --- применимость типа атрибута (голый строковый enum) ---


async def test_attribute_type_applicability_object_type(fake_ips: FakeIPS) -> None:
    fake_ips.add("get", "/core/api/metadata/attributeTypeApplicability/1029", body="objectType")
    async with _Client(config=_config(fake_ips)) as ips:
        applicability = await ips.attribute_type_applicability(1029)

    assert applicability.root == "objectType"
    assert applicability.kinds == [AttributeApplicabilityKind.OBJECT_TYPE]


async def test_attribute_type_applicability_by_guid_relation_type(fake_ips: FakeIPS) -> None:
    fake_ips.add(
        "get",
        f"/core/api/metadata/attributeTypeApplicability/byGuid/{_GUID}",
        body="relationType",
    )
    async with _Client(config=_config(fake_ips)) as ips:
        applicability = await ips.attribute_type_applicability_by_guid(_GUID)

    assert applicability.kinds == [AttributeApplicabilityKind.RELATION_TYPE]


async def test_attribute_type_applicability_flags_combination(fake_ips: FakeIPS) -> None:
    # Прод-факт: сервер возвращает комбинацию категорий через запятую.
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeTypeApplicability/9",
        body="objectType, relationType",
    )
    async with _Client(config=_config(fake_ips)) as ips:
        applicability = await ips.attribute_type_applicability(9)

    assert applicability.root == "objectType, relationType"
    assert applicability.kinds == [
        AttributeApplicabilityKind.OBJECT_TYPE,
        AttributeApplicabilityKind.RELATION_TYPE,
    ]


async def test_attribute_is_in_use_returns_bool(fake_ips: FakeIPS) -> None:
    fake_ips.add("get", "/core/api/metadata/attributeTypeApplicability/1029/inUse", body=True)
    async with _Client(config=_config(fake_ips)) as ips:
        assert await ips.attribute_is_in_use(1029) is True


async def test_attribute_is_in_use_false_when_null(fake_ips: FakeIPS) -> None:
    fake_ips.add("get", "/core/api/metadata/attributeTypeApplicability/1029/inUse", body=None)
    async with _Client(config=_config(fake_ips)) as ips:
        assert await ips.attribute_is_in_use(1029) is False


async def test_attribute_is_in_use_by_guid_returns_bool(fake_ips: FakeIPS) -> None:
    fake_ips.add(
        "get",
        f"/core/api/metadata/attributeTypeApplicability/byGuid/{_GUID}/inUse",
        body=False,
    )
    async with _Client(config=_config(fake_ips)) as ips:
        assert await ips.attribute_is_in_use_by_guid(_GUID) is False


# --- атрибут-ссылка и связанные типы объектов ---


async def test_attribute_linked_object_type_ids_unwraps_entity(fake_ips: FakeIPS) -> None:
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeLinkedObjectTypeIds/1029",
        body={"entity": [10, 20], "isEntityPresent": True},
    )
    async with _Client(config=_config(fake_ips)) as ips:
        ids = await ips.attribute_linked_object_type_ids(1029)

    assert ids == [10, 20]
    assert all(isinstance(i, int) for i in ids)


async def test_attribute_linked_object_type_ids_none_when_absent(fake_ips: FakeIPS) -> None:
    fake_ips.add(
        "get",
        "/core/api/metadata/attributeLinkedObjectTypeIds/1029",
        body={"entity": None, "isEntityPresent": False},
    )
    async with _Client(config=_config(fake_ips)) as ips:
        assert await ips.attribute_linked_object_type_ids(1029) is None


async def test_object_link_attribute_type_ids_returns_list(fake_ips: FakeIPS) -> None:
    fake_ips.add("get", "/core/api/metadata/objectLinkAttributeTypeIds/1742", body=[1029, 1030])
    async with _Client(config=_config(fake_ips)) as ips:
        assert await ips.object_link_attribute_type_ids(1742) == [1029, 1030]


# --- разрозненные справки ---


async def test_relation_type_for_prj_link_returns_int(fake_ips: FakeIPS) -> None:
    fake_ips.add("get", "/core/api/metadata/relationTypeForPrjLink/12345", body=7)
    async with _Client(config=_config(fake_ips)) as ips:
        result = await ips.relation_type_for_prj_link(12345)

    assert result == 7
    assert isinstance(result, int)


async def test_related_formula_attributes_for_object_returns_list(fake_ips: FakeIPS) -> None:
    fake_ips.add(
        "get",
        "/core/api/metadata/relatedFormulaAttributesForObject/1742/1029",
        body=[2001, 2002],
    )
    async with _Client(config=_config(fake_ips)) as ips:
        ids = await ips.related_formula_attributes_for_object(1742, 1029)

    assert ids == [2001, 2002]
    assert fake_ips.requests[-1].path == (
        "/core/api/metadata/relatedFormulaAttributesForObject/1742/1029"
    )


async def test_related_formula_attributes_for_relation_returns_list(fake_ips: FakeIPS) -> None:
    fake_ips.add(
        "get",
        "/core/api/metadata/relatedFormulaAttributesForRelation/7/1029",
        body=[3001],
    )
    async with _Client(config=_config(fake_ips)) as ips:
        assert await ips.related_formula_attributes_for_relation(7, 1029) == [3001]
