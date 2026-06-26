"""Методы раздела управления проектами (Improject) IPS Web API."""

from .change_task_progress import ChangeTaskProgressMixin
from .complete_project import CompleteProjectMixin
from .create_dependency import CreateDependencyMixin
from .create_project import CreateProjectMixin
from .create_task import CreateTaskMixin
from .delete_dependency import DeleteDependencyMixin
from .delete_task import DeleteTaskMixin
from .grid_columns import GridColumnsMixin
from .move_task_level_down import MoveTaskLevelDownMixin
from .move_task_level_up import MoveTaskLevelUpMixin
from .project import ProjectMixin
from .reorder_task import ReorderTaskMixin
from .resource_assignments import ResourceAssignmentsMixin
from .save_approval_result import SaveApprovalResultMixin
from .save_project_zoom_level import SaveProjectZoomLevelMixin
from .start_executing_project import StartExecutingProjectMixin
from .start_executing_task import StartExecutingTaskMixin
from .stop_executing_project import StopExecutingProjectMixin
from .task import TaskMixin
from .task_attachments import TaskAttachmentsMixin
from .task_attachments_allowed_types import TaskAttachmentsAllowedTypesMixin
from .update_dependency import UpdateDependencyMixin
from .update_grid_columns import UpdateGridColumnsMixin
from .update_task import UpdateTaskMixin


class ImProjectsAPI(
    ProjectMixin,
    TaskMixin,
    TaskAttachmentsMixin,
    ResourceAssignmentsMixin,
    GridColumnsMixin,
    TaskAttachmentsAllowedTypesMixin,
    # мутации Gantt (create/update/delete/move/execute — confirm)
    CreateProjectMixin,
    CreateTaskMixin,
    CreateDependencyMixin,
    UpdateTaskMixin,
    DeleteTaskMixin,
    UpdateDependencyMixin,
    DeleteDependencyMixin,
    MoveTaskLevelDownMixin,
    MoveTaskLevelUpMixin,
    ReorderTaskMixin,
    ChangeTaskProgressMixin,
    SaveApprovalResultMixin,
    StartExecutingTaskMixin,
    StartExecutingProjectMixin,
    StopExecutingProjectMixin,
    CompleteProjectMixin,
    SaveProjectZoomLevelMixin,
    UpdateGridColumnsMixin,
):
    """Объединяет методы чтения раздела управления проектами (Improject).

    References:
        Эндпоинты ``/core/api/improjects/*`` IPS Server Web API.
    """


__all__ = ["ImProjectsAPI"]
