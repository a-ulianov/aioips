"""Методы раздела файловых систем IPS Web API."""

from .create_directory import CreateDirectoryMixin
from .find_directories import FindDirectoriesMixin
from .find_files import FindFilesMixin
from .is_directory_exists import IsDirectoryExistsMixin
from .local_drives import LocalDrivesMixin


class FileSystemsAPI(
    LocalDrivesMixin,
    FindDirectoriesMixin,
    FindFilesMixin,
    IsDirectoryExistsMixin,
    CreateDirectoryMixin,
):
    """Объединяет методы раздела файловых систем.

    References:
        Эндпоинты ``/core/api/fileSystems/*`` IPS Server Web API.
    """


__all__ = ["FileSystemsAPI"]
