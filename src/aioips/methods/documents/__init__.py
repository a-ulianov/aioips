"""Методы раздела документов IPS Web API."""

from .create_document_prototypes import CreateDocumentPrototypesMixin
from .document_prototypes_common import DocumentPrototypesCommonMixin
from .document_prototypes_private import DocumentPrototypesPrivateMixin
from .document_settings import DocumentSettingsMixin
from .save_document_settings import SaveDocumentSettingsMixin
from .update_document_prototypes import UpdateDocumentPrototypesMixin


class DocumentsAPI(
    DocumentPrototypesCommonMixin,
    DocumentPrototypesPrivateMixin,
    DocumentSettingsMixin,
    SaveDocumentSettingsMixin,
    CreateDocumentPrototypesMixin,
    UpdateDocumentPrototypesMixin,
):
    """Объединяет методы раздела документов.

    References:
        Эндпоинты ``/api/documents/*`` IPS Server Web API.
    """


__all__ = ["DocumentsAPI"]
