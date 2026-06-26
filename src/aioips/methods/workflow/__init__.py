"""Методы раздела процессов (workflow) IPS Web API."""

from .wf_add_attachments import WFAddAttachmentsMixin
from .wf_attach_files import WFAttachFilesMixin
from .wf_attachment_allowed_types import WFAttachmentAllowedTypesMixin
from .wf_attachments import WFAttachmentsMixin
from .wf_attachments_data import WFAttachmentsDataMixin
from .wf_create_attach_files import WFCreateAttachFilesMixin
from .wf_remove_attachments import WFRemoveAttachmentsMixin
from .wf_save_variables import WFSaveVariablesMixin
from .wf_variables import WFVariablesMixin


class WorkflowAPI(
    WFAttachmentsMixin,
    WFAttachmentAllowedTypesMixin,
    WFVariablesMixin,
    WFSaveVariablesMixin,
    WFAddAttachmentsMixin,
    WFRemoveAttachmentsMixin,
    WFAttachmentsDataMixin,
    WFAttachFilesMixin,
    WFCreateAttachFilesMixin,
):
    """Объединяет методы чтения раздела процессов (workflow).

    References:
        Эндпоинты ``/core/api/wfAttachments/*`` и ``/core/api/wfVariables/*``
        IPS Server Web API.
    """


__all__ = ["WorkflowAPI"]
