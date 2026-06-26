"""Перечисления раздела файлов IPS Web API."""

from enum import StrEnum


class FileTypes(StrEnum):
    """Тип файла в файловом атрибуте объекта (``ftFile``).

    Значения соответствуют enum ``FileTypes`` swagger. Используется в
    :meth:`~aioips.IPSClient.add_object_file` (поле формы ``fileType``).

    Attributes:
        NORMAL: Обычный файл объекта (``ftNormal``).
        NOT_CONTENT: Файл, не относящийся к контенту (``ftNotContent``).
        OTD: Файл ОТД (``ftOTD``).
        REDLINING: Файл редактуры/пометок (``ftRedlining``).
        AUTHENTICAL: Аутентичный файл (``ftAuthentical``).
        UNKNOWN: Неизвестный тип (``ftUnknown``).
    """

    NORMAL = "ftNormal"
    NOT_CONTENT = "ftNotContent"
    OTD = "ftOTD"
    REDLINING = "ftRedlining"
    AUTHENTICAL = "ftAuthentical"
    UNKNOWN = "ftUnknown"
