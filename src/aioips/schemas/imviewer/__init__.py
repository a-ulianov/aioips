"""Схемы раздела 3D-просмотрщика (ImViewer) IPS Web API."""

from .assembly import Assembly
from .assembly_composition import (
    ImViewerAssemblyCompositionTreeNode,
    SourceAssemblyCompositionTreeNode,
)
from .mesh import Mesh
from .object_info import ImViewerObjectInfo

__all__ = [
    "Assembly",
    "ImViewerAssemblyCompositionTreeNode",
    "ImViewerObjectInfo",
    "Mesh",
    "SourceAssemblyCompositionTreeNode",
]
