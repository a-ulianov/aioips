"""Схемы раздела файлов IPS Web API."""

from .attach_temp_file import AttachTempFile
from .data_table import DataTableDto
from .files_table_params import (
    ObjectIdsWithColumnsDto,
    ObjectIdsWithColumnsFileNameDto,
    ObjectSnapshotIds,
)
from .object_files_tree import ObjectFilesTreeNodeDto
from .object_with_file_attributes import (
    BlobFileAttributeInfo,
    FileAttribute,
    ObjectWithFileAttributes,
)
from .prototype_info import PrototypeInfo
from .swap_files import SwapFiles
from .update_object_file_info import UpdateObjectFileInfo

__all__ = [
    "AttachTempFile",
    "BlobFileAttributeInfo",
    "DataTableDto",
    "FileAttribute",
    "ObjectFilesTreeNodeDto",
    "ObjectIdsWithColumnsDto",
    "ObjectIdsWithColumnsFileNameDto",
    "ObjectSnapshotIds",
    "ObjectWithFileAttributes",
    "PrototypeInfo",
    "SwapFiles",
    "UpdateObjectFileInfo",
]
