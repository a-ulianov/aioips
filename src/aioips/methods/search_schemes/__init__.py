"""Методы раздела поисковых схем (выборок) IPS Web API."""

from .condition_structure_info import ConditionStructureInfoMixin
from .edit_search_scheme import EditSearchSchemeMixin
from .search_scheme import SearchSchemeMixin


class SearchSchemesAPI(
    SearchSchemeMixin,
    ConditionStructureInfoMixin,
    EditSearchSchemeMixin,
):
    """Объединяет методы раздела поисковых схем (выборок).

    References:
        Эндпоинты ``/core/api/searchSchemes/*`` IPS Server Web API.
    """


__all__ = ["SearchSchemesAPI"]
