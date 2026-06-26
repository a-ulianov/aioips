"""Схемы раздела объектов IPS Web API."""

from .add_objects_by_template import AddObjectsByTemplateBody
from .attribute import Attribute, AttributeValues
from .composition_params import AllObjectVersionsParameters, ObjectCompositionParams
from .create_by_prototype import CreateObjectByPrototype
from .object import ObjectDto, QuickObjectInfo
from .objects_select_request import (
    ObjectSelectByIdDTO,
    ObjectSelectDTO,
    ObjectSelectRequest,
)
from .select import AttributeResult, ObjectSelectResult, SelectCondition
from .set_attribute_values_ex import SetAttributeValuesExBody
from .snapshot_info import ObjectSnapshot, SnapshotInfo
from .write_result import ModificationEntry

__all__ = [
    "AddObjectsByTemplateBody",
    "AllObjectVersionsParameters",
    "Attribute",
    "AttributeResult",
    "AttributeValues",
    "CreateObjectByPrototype",
    "ModificationEntry",
    "ObjectCompositionParams",
    "ObjectDto",
    "ObjectSelectByIdDTO",
    "ObjectSelectDTO",
    "ObjectSelectRequest",
    "ObjectSelectResult",
    "ObjectSnapshot",
    "QuickObjectInfo",
    "SelectCondition",
    "SetAttributeValuesExBody",
    "SnapshotInfo",
]
