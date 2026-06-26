"""Схемы раздела документов IPS Web API."""

from .document_prototype import DocumentPrototype
from .document_settings import DocumentSettings, DocumentSettingsSubscriber

__all__ = ["DocumentPrototype", "DocumentSettings", "DocumentSettingsSubscriber"]
