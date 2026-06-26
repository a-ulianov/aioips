"""Схемы тел запросов загрузки файлов через IPS Bridge.

References:
    ``POST /core/api/Bridge/Files/UploadFile`` — ``FileRequestDTO``;
    ``POST /core/api/Bridge/Files/UploadLargeFileRequest`` — ``LargeFileRequestDTO``;
    ``POST /core/api/Bridge/Files/UploadLargeFileChunk`` — ``LargeFileChunkDTO``;
    ``POST /core/api/Bridge/Files/UploadLargeFileChunkBase64`` — ``LargeFileChunkDTOBase64``.
"""

from uuid import UUID

from pydantic import Field

from ..base import IPSModel


class FileRequestDTO(IPSModel):
    """Тело запроса загрузки целого файла во временное хранилище IPS Bridge.

    Используется методом :meth:`bridge_upload_file` для передачи небольшого
    файла одним запросом. Содержимое кодируется в Base64 в поле ``data``.

    Attributes:
        data: Содержимое файла в Base64 (``None`` — пустой файл).
        file_name: Имя файла (``None`` — имя по умолчанию на сервере).
        content: Дополнительное текстовое содержимое/метаданные (``None``).
    """

    data: str | None = Field(default=None, description="Содержимое файла в Base64")
    file_name: str | None = Field(default=None, description="Имя файла")
    content: str | None = Field(default=None, description="Текстовое содержимое/метаданные")


class LargeFileRequestDTO(IPSModel):
    """Тело инициализации загрузки большого файла по частям через IPS Bridge.

    Используется методом :meth:`bridge_upload_large_file_request`: открывает
    сессию чанковой загрузки, заявляя имя, размер и число частей. В ответ
    сервер возвращает GUID запроса для последующих чанков.

    Attributes:
        file_name: Имя загружаемого файла (``None`` — по умолчанию).
        total_bytes: Полный размер файла в байтах.
        total_chunks: Общее число частей (чанков), на которые разбит файл.
        custom_directory_path: Целевой подкаталог во временном хранилище (``None``).
    """

    file_name: str | None = Field(default=None, description="Имя файла")
    total_bytes: int = Field(default=0, description="Полный размер файла в байтах")
    total_chunks: int = Field(default=0, description="Общее число частей файла")
    custom_directory_path: str | None = Field(
        default=None, description="Целевой подкаталог хранилища"
    )


class LargeFileChunkDTO(IPSModel):
    """Тело передачи одной части большого файла (Base64-байты) через IPS Bridge.

    Используется методом :meth:`bridge_upload_large_file_chunk`: передаёт
    очередной чанк в открытую сессию загрузки (см.
    :meth:`bridge_upload_large_file_request`).

    Attributes:
        request_guid: GUID сессии загрузки, полученный при её инициализации.
        chunk_number: Порядковый номер части (с нуля или единицы — по серверу).
        data: Содержимое части в Base64 (``None`` — пустая часть).
    """

    request_guid: UUID = Field(description="GUID сессии загрузки")
    chunk_number: int = Field(default=0, description="Порядковый номер части")
    data: str | None = Field(default=None, description="Содержимое части в Base64")


class LargeFileChunkDTOBase64(IPSModel):
    """Тело передачи одной части большого файла (строка Base64) через IPS Bridge.

    Вариант :class:`LargeFileChunkDTO` для метода
    :meth:`bridge_upload_large_file_chunk_base64`: поле ``data`` — обычная
    Base64-строка без бинарного формата.

    Attributes:
        request_guid: GUID сессии загрузки, полученный при её инициализации.
        chunk_number: Порядковый номер части.
        data: Содержимое части в виде Base64-строки (``None`` — пустая часть).
    """

    request_guid: UUID = Field(description="GUID сессии загрузки")
    chunk_number: int = Field(default=0, description="Порядковый номер части")
    data: str | None = Field(default=None, description="Содержимое части (Base64-строка)")
