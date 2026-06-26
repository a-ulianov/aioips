"""Схема параметров перестановки двух файлов в файловом атрибуте объекта.

References:
    ``POST /core/api/files/objects/{objectId}/files/swap`` — тело ``SwapFiles``
    (operationId ``Files_SwapFilesInAttr``).
"""

from pydantic import Field

from ..base import IPSModel


class SwapFiles(IPSModel):
    """Параметры перестановки (swap) двух файлов внутри файлового атрибута.

    Описывает желаемую перестановку файлов в МНОЖЕСТВЕННОМ файловом атрибуте
    (``ftFile`` с ``is_multiple=True``): файл, находящийся на позиции
    ``old_position``, перемещается на позицию ``change_position`` (и наоборот),
    что меняет ПОРЯДОК файлов в атрибуте. Контент файлов не затрагивается —
    меняется только их взаимное расположение. ``attribute_id`` указывает, в
    каком файловом атрибуте выполняется перестановка; ``blob_id`` адресует
    переставляемый файл (BLOB-запись).

    Операция симметрична и обратима: повторный вызов с переставленными
    ``old_position`` и ``change_position`` возвращает исходный порядок.

    Все поля имеют дефолт ``0`` (DTO не помечает их required), поэтому при
    формировании тела задавайте значимые поля явно.

    Attributes:
        old_position: Исходная позиция файла в атрибуте (DTO ``oldPosition``,
            int32); индекс файла до перестановки.
        attribute_id: Идентификатор файлового атрибута (``ftFile``); DTO
            ``attributeId`` (int32).
        blob_id: Идентификатор переставляемой BLOB-записи (DTO ``blobId``,
            int64); адресует конкретный файл атрибута.
        change_position: Целевая позиция файла после перестановки (DTO
            ``changePosition``, int32); индекс, на который перемещается файл.
    """

    old_position: int = Field(default=0, description="Исходная позиция файла в атрибуте")
    attribute_id: int = Field(default=0, description="Идентификатор файлового атрибута")
    blob_id: int = Field(default=0, description="Идентификатор переставляемой BLOB-записи")
    change_position: int = Field(default=0, description="Целевая позиция файла после перестановки")
