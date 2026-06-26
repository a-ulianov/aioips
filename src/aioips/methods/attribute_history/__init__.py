"""Методы раздела истории значений атрибутов IPS Web API."""

from .attribute_history import AttributeHistoryMixin
from .delete_attribute_history import DeleteAttributeHistoryMixin


class AttributeHistoryAPI(AttributeHistoryMixin, DeleteAttributeHistoryMixin):
    """Объединяет методы раздела истории значений атрибутов.

    References:
        Эндпоинты ``/core/api/attributeHistory/*`` IPS Server Web API.
    """


__all__ = ["AttributeHistoryAPI"]
