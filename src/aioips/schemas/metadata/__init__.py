"""Схемы раздела метаданных IPS Web API."""

from .applicability import ObjectTypeApplicability
from .attribute_for_object_type import AttributeForObjectType
from .attribute_for_relation_type import AttributeForRelationType
from .attribute_group import AttributeGroup
from .attribute_type_applicability import (
    AttributeApplicabilityKind,
    AttributeTypeApplicability,
)
from .attribute_types import AttributeType
from .life_cycle_level import LifeCycleLevel
from .life_cycle_scheme import LifeCycleScheme
from .life_cycle_step import LifeCycleStep
from .object_types import ObjectType
from .relation_type_meta import RelationTypeMeta

__all__ = [
    "AttributeApplicabilityKind",
    "AttributeForObjectType",
    "AttributeForRelationType",
    "AttributeGroup",
    "AttributeType",
    "AttributeTypeApplicability",
    "LifeCycleLevel",
    "LifeCycleScheme",
    "LifeCycleStep",
    "ObjectType",
    "ObjectTypeApplicability",
    "RelationTypeMeta",
]
