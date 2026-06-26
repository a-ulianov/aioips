"""Методы раздела связей IPS Web API."""

from .relation_add_temporary_attribute import RelationAddTemporaryAttributeMixin
from .relation_attribute import RelationAttributeMixin
from .relation_attribute_descriptions import RelationAttributeDescriptionsMixin
from .relation_attribute_values import RelationAttributeValuesMixin
from .relation_attributes import RelationAttributesMixin
from .relation_attributes_descriptions import RelationAttributesDescriptionsMixin
from .relation_attributes_init_values import RelationAttributesInitValuesMixin
from .relation_attributes_values import RelationAttributesValuesMixin
from .relation_by_guid_and_project import RelationByGuidAndProjectMixin
from .relation_by_project_and_part import RelationByProjectAndPartMixin
from .relation_create import RelationCreateMixin
from .relation_create_collection import RelationCreateCollectionMixin
from .relation_delete import RelationDeleteMixin
from .relation_delete_attribute import RelationDeleteAttributeMixin
from .relation_get import RelationGetMixin
from .relation_get_by_guid import RelationGetByGuidMixin
from .relation_set_attribute_values import RelationSetAttributeValuesMixin
from .relation_set_attribute_values_ex import RelationSetAttributeValuesExMixin
from .relation_set_attributes import RelationSetAttributesMixin
from .relation_types import RelationTypesMixin
from .relation_update_relations_attributes import RelationUpdateRelationsAttributesMixin
from .relations_by_project import RelationsByProjectMixin
from .relations_consist_from import RelationsConsistFromMixin
from .relations_enters_in import RelationsEntersInMixin
from .relations_enters_in_version import RelationsEntersInVersionMixin
from .relations_request import (
    RelationsConsistFromRequestMixin,
    RelationsEntersInVersionRequestMixin,
)
from .relations_select import RelationsSelectMixin


class RelationsAPI(
    RelationGetMixin,
    RelationGetByGuidMixin,
    RelationsByProjectMixin,
    RelationTypesMixin,
    RelationAttributesMixin,
    RelationAttributeMixin,
    RelationAttributeValuesMixin,
    RelationAttributesValuesMixin,
    RelationSetAttributesMixin,
    RelationSetAttributeValuesMixin,
    RelationSetAttributeValuesExMixin,
    RelationUpdateRelationsAttributesMixin,
    RelationAddTemporaryAttributeMixin,
    RelationByGuidAndProjectMixin,
    RelationByProjectAndPartMixin,
    RelationAttributeDescriptionsMixin,
    RelationAttributesDescriptionsMixin,
    RelationAttributesInitValuesMixin,
    RelationCreateMixin,
    RelationCreateCollectionMixin,
    RelationDeleteMixin,
    RelationDeleteAttributeMixin,
    RelationsConsistFromMixin,
    RelationsEntersInMixin,
    RelationsEntersInVersionMixin,
    RelationsConsistFromRequestMixin,
    RelationsEntersInVersionRequestMixin,
    RelationsSelectMixin,
):
    """Объединяет методы раздела связей (чтение связей, их типов и атрибутов).

    References:
        Эндпоинты ``/core/api/relations/*`` IPS Server Web API.
    """


__all__ = ["RelationsAPI"]
