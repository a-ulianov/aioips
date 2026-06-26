"""Методы-разделы IPS Web API, собираемые в единый клиент."""

from .archives import ArchivesAPI
from .attribute_history import AttributeHistoryAPI
from .auth import AuthAPI
from .bridge import BridgeAPI
from .briefcase import BriefcaseAPI
from .calendars import CalendarsAPI
from .config import ConfigAPI
from .crypto_signing import CryptoSigningAPI
from .discussions import DiscussionsAPI
from .docs import DocsAPI
from .document_editor import DocumentEditorAPI
from .documents import DocumentsAPI
from .editing_contexts import EditingContextsAPI
from .file_systems import FileSystemsAPI
from .files import FilesAPI
from .forms import FormsAPI
from .graph_signs import GraphSignsAPI
from .imbase import ImBaseAPI
from .improjects import ImProjectsAPI
from .imviewer import ImViewerAPI
from .licenses import LicensesAPI
from .mail_agent import MailAgentAPI
from .measure_units import MeasureUnitsAPI
from .metadata import MetadataAPI
from .notify import NotifyAPI
from .object_types import ObjectTypesAPI
from .objects import ObjectsAPI
from .relation_queries import RelationQueriesAPI
from .relation_types import RelationTypesAPI
from .relations import RelationsAPI
from .samples import SamplesAPI
from .search_schemes import SearchSchemesAPI
from .security import SecurityAPI
from .selection_classificators import SelectionClassificatorsAPI
from .settings import SettingsAPI
from .signs import SignsAPI
from .snapshots import SnapshotsAPI
from .sso import SsoAPI
from .table_report import TableReportAPI
from .users import UsersAPI
from .visibilities import VisibilitiesAPI
from .workflow import WorkflowAPI

__all__ = [
    "ArchivesAPI",
    "AttributeHistoryAPI",
    "AuthAPI",
    "BridgeAPI",
    "BriefcaseAPI",
    "CalendarsAPI",
    "ConfigAPI",
    "CryptoSigningAPI",
    "DiscussionsAPI",
    "DocsAPI",
    "DocumentEditorAPI",
    "DocumentsAPI",
    "EditingContextsAPI",
    "FileSystemsAPI",
    "FilesAPI",
    "FormsAPI",
    "GraphSignsAPI",
    "ImBaseAPI",
    "ImProjectsAPI",
    "ImViewerAPI",
    "LicensesAPI",
    "MailAgentAPI",
    "MeasureUnitsAPI",
    "MetadataAPI",
    "NotifyAPI",
    "ObjectTypesAPI",
    "ObjectsAPI",
    "RelationQueriesAPI",
    "RelationTypesAPI",
    "RelationsAPI",
    "SamplesAPI",
    "SearchSchemesAPI",
    "SecurityAPI",
    "SelectionClassificatorsAPI",
    "SettingsAPI",
    "SignsAPI",
    "SnapshotsAPI",
    "SsoAPI",
    "TableReportAPI",
    "UsersAPI",
    "VisibilitiesAPI",
    "WorkflowAPI",
]
