"""Методы раздела docs (типы и настройки документов) IPS Web API."""

from .doc_settings import DocSettingsMixin
from .doc_settings_list import DocSettingsListMixin
from .doc_suffixes import DocSuffixesMixin
from .document_types_by_file_ext import DocumentTypesByFileExtMixin
from .document_types_by_output_object_types import DocumentTypesByOutputObjectTypesMixin
from .inherited_from_constructor_documents import InheritedFromConstructorDocumentsMixin
from .inherited_from_documents import InheritedFromDocumentsMixin
from .set_doc_settings import SetDocSettingsMixin


class DocsAPI(
    DocSuffixesMixin,
    DocumentTypesByFileExtMixin,
    DocumentTypesByOutputObjectTypesMixin,
    DocSettingsMixin,
    DocSettingsListMixin,
    InheritedFromConstructorDocumentsMixin,
    InheritedFromDocumentsMixin,
    SetDocSettingsMixin,
):
    """Объединяет методы раздела docs.

    References:
        Эндпоинты ``/core/api/docs/*`` IPS Server Web API.
    """


__all__ = ["DocsAPI"]
