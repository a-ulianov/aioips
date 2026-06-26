"""Методы раздела контекстов редактирования IPS Web API."""

from .add_objects_to_editing_context import AddObjectsToEditingContextMixin
from .replace_version_in_editing_context import ReplaceVersionInEditingContextMixin
from .update_editing_context_objects import UpdateEditingContextObjectsMixin


class EditingContextsAPI(
    AddObjectsToEditingContextMixin,
    ReplaceVersionInEditingContextMixin,
    UpdateEditingContextObjectsMixin,
):
    """Объединяет методы раздела контекстов редактирования.

    References:
        Эндпоинты ``/core/api/editingContexts/*`` IPS Server Web API.
    """


__all__ = ["EditingContextsAPI"]
