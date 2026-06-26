"""Схемы раздела управления проектами (Improject) IPS Web API."""

from .attachment import Attachment
from .displayed_columns import DisplayedColumns
from .project import Project
from .resource_assignments import ResourceAssignments
from .scale_type import ScaleType
from .task import Task

__all__ = [
    "Attachment",
    "DisplayedColumns",
    "Project",
    "ResourceAssignments",
    "ScaleType",
    "Task",
]
