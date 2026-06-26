"""Перечисления доменных значений IPS Web API."""

from .attribute import ComputeValueMode, FieldType, MultiValueMode
from .auth import AuthPasswordType
from .document_editor import OpenDocumentMode
from .files import FileTypes
from .imbase import SearchesAccuracy
from .metadata import InheritMode, ObjectsClassifyType, ObjectVersionMode
from .objects import ObjectModifyMode
from .select import ColumnContent, LogicalOperator, RelationalOperator

__all__ = [
    "AuthPasswordType",
    "ColumnContent",
    "ComputeValueMode",
    "FieldType",
    "FileTypes",
    "InheritMode",
    "LogicalOperator",
    "MultiValueMode",
    "ObjectModifyMode",
    "ObjectVersionMode",
    "ObjectsClassifyType",
    "OpenDocumentMode",
    "RelationalOperator",
    "SearchesAccuracy",
]
