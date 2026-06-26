"""Схема описания временного файла для прикрепления к атрибуту объекта.

References:
    DTO ``AttachTempFileToAttribute`` — элемент тела
    ``POST /core/api/files/objects/{objectId}/attachTempFiles``
    (operationId ``Files_AttachTempFilesToAttributes``).
"""

from datetime import datetime

from pydantic import Field

from ..base import IPSModel


class AttachTempFile(IPSModel):
    """Описание одного временного файла, прикрепляемого к файловому атрибуту.

    Используется при прикреплении уже загруженных временных файлов (результат
    :meth:`upload_temp_file`) к файловым атрибутам (``ftFile``) объекта через
    метод ``attach_temp_files``. Каждый элемент связывает временный файл из
    временного хранилища IPS с конкретным файловым атрибутом объекта.

    ПРЕДУСЛОВИЕ: ``temp_file_name`` должен быть именем, ранее возвращённым
    :meth:`upload_temp_file`; ``attribute_id`` — идентификатором ИМЕННО
    файлового атрибута (``ftFile``) объекта, к которому прикрепляется файл.
    Прикрепление выполняется в рамках жизненного цикла редактирования объекта
    (checkout), как и прочие операции записи.

    Attributes:
        attribute_id: Идентификатор файлового атрибута объекта (DTO
            ``attributeId``, int32), к которому прикрепляется файл. Обязательно.
        temp_file_name: Имя временного файла во временном хранилище IPS (DTO
            ``tempFileName``), полученное из :meth:`upload_temp_file`.
            Обязательно, непустая строка.
        file_type: Тип файла (DTO ``fileType``, перечисление ``FileTypes``):
            ``ftNormal`` — файл объекта; ``ftNotContent`` — файл, не влияющий на
            подписи; ``ftOTD`` — файл ОТД; ``ftRedlining`` — файл замечаний;
            ``ftAuthentical`` — аутентичный файл; ``ftUnknown`` — неизвестный.
            Моделируется строкой (как в :class:`FileAttribute`). Обязательно.
        modify_date_time: Дата модификации файла (BLOB-поля) в ЛОКАЛЬНОМ времени
            (DTO ``modifyDateTime``). Сервер округляет до секунд для корректного
            сравнения версий. Обязательно.
        real_file_size: Реальный размер файла в байтах (DTO ``realFileSize``,
            int64). Если не ``None`` — файл уже упакован. Обязательно.
    """

    attribute_id: int = Field(description="Идентификатор файлового атрибута объекта")
    temp_file_name: str = Field(
        min_length=1, description="Имя временного файла во временном хранилище IPS"
    )
    file_type: str = Field(description="Тип файла (перечисление FileTypes)")
    modify_date_time: datetime = Field(description="Дата модификации файла в локальном времени")
    real_file_size: int = Field(description="Реальный размер файла в байтах")
