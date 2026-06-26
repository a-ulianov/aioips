"""Схемы раздела поисковых схем (выборок) IPS Web API."""

from .condition_structure_info import ConditionStructureInfo
from .search_scheme import (
    AttributeSourceType,
    SearchSchemaAdditionalColumn,
    SearchScheme,
)

__all__ = [
    "AttributeSourceType",
    "ConditionStructureInfo",
    "SearchSchemaAdditionalColumn",
    "SearchScheme",
]
