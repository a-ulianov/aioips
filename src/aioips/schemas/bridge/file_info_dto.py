"""Схема сведений о файле, упакованном/созданном IPS Bridge.

References:
    ``POST /core/api/Bridge/Files/PackDirectoryAsZip`` — ``FileInfoDto``.
"""

from pydantic import Field

from ..base import IPSModel


class FileInfoDto(IPSModel):
    """Сведения о файле во временном хранилище сессии IPS Bridge.

    IPS Bridge — серверный помощник десктоп-клиента; он умеет создавать в
    рамках сессии временные файлы (например, ZIP-архив каталога). Схема несёт
    путь к такому файлу и его размер. Применяйте, чтобы получить ссылку на
    результат упаковки каталога (:meth:`bridge_pack_directory_as_zip`) перед
    его скачиванием или удалением через :meth:`bridge_delete_temp_stored_item`.

    Attributes:
        file_path: Серверный путь к файлу. ``None``, если сервер не вернул путь.
        total_bytes: Полный размер файла в байтах. ``0``, если размер не задан.
    """

    file_path: str | None = Field(default=None, description="Серверный путь к файлу")
    total_bytes: int = Field(default=0, description="Полный размер файла в байтах")
