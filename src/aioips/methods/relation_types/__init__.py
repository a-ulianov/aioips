"""Методы раздела типов связей IPS Web API."""

from .relation_type_relation_ids import RelationTypeRelationIdsMixin
from .relation_type_relations import RelationTypeRelationsMixin


class RelationTypesAPI(RelationTypeRelationsMixin, RelationTypeRelationIdsMixin):
    """Объединяет методы раздела типов связей.

    References:
        Эндпоинты ``/core/api/relationTypes/*`` IPS Server Web API.
    """


__all__ = ["RelationTypesAPI"]
