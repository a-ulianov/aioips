"""Методы раздела файлов IPS Web API."""

from .add_object_file import AddObjectFileMixin
from .attach_temp_files import AttachTempFilesMixin
from .check_unique_file_names import CheckUniqueFileNamesMixin
from .delete_object_file import DeleteObjectFileMixin
from .delete_temp_file import DeleteTempFileMixin
from .file_attributes import FileAttributesMixin
from .file_id_by_name import FileIdByNameMixin
from .file_prototypes import FilePrototypesMixin
from .file_unique_name import FileUniqueNameMixin
from .get_file_name_table import GetFileNameTableMixin
from .get_file_names_table import GetFileNamesTableMixin
from .get_files_table import GetFilesTableMixin
from .get_files_table_all_attributes import GetFilesTableAllAttributesMixin
from .get_files_table_by_fields import GetFilesTableByFieldsMixin
from .get_files_table_with_snapshot_ids import GetFilesTableWithSnapshotIdsMixin
from .handle_file_attributes_for_object_creation import (
    HandleFileAttributesForObjectCreationMixin,
)
from .next_file_id import NextFileIdMixin
from .object_file_by_blob_id import ObjectFileByBlobIdMixin
from .object_file_by_name import ObjectFileByNameMixin
from .object_files_with_composition import ObjectFilesWithCompositionMixin
from .object_ids_by_file_name import ObjectIdsByFileNameMixin
from .set_file_attr_prototype import SetFileAttrPrototypeMixin
from .set_prototype import SetPrototypeMixin
from .swap_object_files import SwapObjectFilesMixin
from .update_object_file import UpdateObjectFileMixin
from .update_object_file_info import UpdateObjectFileInfoMixin
from .upload_temp_file import UploadTempFileMixin


class FilesAPI(
    FilePrototypesMixin,
    FileAttributesMixin,
    ObjectFileByNameMixin,
    ObjectFileByBlobIdMixin,
    UploadTempFileMixin,
    DeleteTempFileMixin,
    FileUniqueNameMixin,
    NextFileIdMixin,
    FileIdByNameMixin,
    ObjectIdsByFileNameMixin,
    AttachTempFilesMixin,
    GetFileNameTableMixin,
    GetFileNamesTableMixin,
    GetFilesTableMixin,
    GetFilesTableByFieldsMixin,
    GetFilesTableAllAttributesMixin,
    GetFilesTableWithSnapshotIdsMixin,
    CheckUniqueFileNamesMixin,
    ObjectFilesWithCompositionMixin,
    AddObjectFileMixin,
    UpdateObjectFileMixin,
    UpdateObjectFileInfoMixin,
    DeleteObjectFileMixin,
    SwapObjectFilesMixin,
    SetFileAttrPrototypeMixin,
    SetPrototypeMixin,
    HandleFileAttributesForObjectCreationMixin,
):
    """Объединяет методы раздела файлов.

    References:
        Эндпоинты ``/core/api/files/*`` IPS Server Web API.
    """


__all__ = ["FilesAPI"]
