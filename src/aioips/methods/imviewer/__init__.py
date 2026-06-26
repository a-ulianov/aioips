"""Методы раздела 3D-просмотрщика (ImViewer) IPS Web API."""

from .imviewer_assembly import ImViewerAssemblyMixin
from .imviewer_assembly_composition import ImViewerAssemblyCompositionMixin
from .imviewer_mesh import ImViewerMeshMixin
from .imviewer_object_info import ImViewerObjectInfoMixin


class ImViewerAPI(
    ImViewerMeshMixin,
    ImViewerAssemblyMixin,
    ImViewerObjectInfoMixin,
    ImViewerAssemblyCompositionMixin,
):
    """Объединяет методы раздела 3D-просмотрщика (данные сетки/сборки/инфо по объекту).

    References:
        Эндпоинты ``/core/api/imviewer/*`` IPS Server Web API.
    """


__all__ = ["ImViewerAPI"]
