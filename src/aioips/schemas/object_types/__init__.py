"""Схемы раздела типов объектов (контроллер ``objectTypes``) IPS Web API."""

from .composition import ObjectsCompositionParams, ObjectWithCompositionDto
from .object_type_definition import ObjectTypeDefinition
from .object_type_objects_info import ObjectTypeObjectsInfo
from .quick_object_type_info import QuickObjectTypeInfo

__all__ = [
    "ObjectTypeDefinition",
    "ObjectTypeObjectsInfo",
    "ObjectWithCompositionDto",
    "ObjectsCompositionParams",
    "QuickObjectTypeInfo",
]
