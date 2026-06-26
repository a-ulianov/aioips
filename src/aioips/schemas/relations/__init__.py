"""Схемы раздела связей IPS Web API."""

from .create_relation import CreateRelation
from .relation import Relation, RelationType
from .relation_collection_request import ObjectRelationDTO, RelationCollectionRequest
from .relations_select import (
    ObjectRelationsSelectParameters,
    RelationSelectAttributeResult,
    RelationSelectResult,
    RelationsSelectParameters,
)

__all__ = [
    "CreateRelation",
    "ObjectRelationDTO",
    "ObjectRelationsSelectParameters",
    "Relation",
    "RelationCollectionRequest",
    "RelationSelectAttributeResult",
    "RelationSelectResult",
    "RelationType",
    "RelationsSelectParameters",
]
