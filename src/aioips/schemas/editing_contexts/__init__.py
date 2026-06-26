"""Схемы раздела контекстов редактирования IPS Web API."""

from .add_objects_to_context import AddObjectsToContext, AddObjectsToEditingContextType
from .add_objects_to_context_result import AddObjectsToContextResult
from .replace_version_in_editing_context import ReplaceVersionInEditingContext
from .update_editing_context_objects_in import UpdateEditingContextObjectsIn

__all__ = [
    "AddObjectsToContext",
    "AddObjectsToContextResult",
    "AddObjectsToEditingContextType",
    "ReplaceVersionInEditingContext",
    "UpdateEditingContextObjectsIn",
]
