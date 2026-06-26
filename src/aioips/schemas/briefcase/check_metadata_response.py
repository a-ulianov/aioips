"""Схема результата проверки метаданных Портфеля IPS.

References:
    ``POST /core/api/briefcase/CheckMetadataResult`` — объект ``CheckMetadataResponseDTO``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class CheckMetadataResponse(IPSModel):
    """Результат фоновой проверки совместимости метаданных Портфеля.

    Перед импортом Портфеля сервер сверяет метаданные пакета (типы, атрибуты, словари)
    с метаданными базы-приёмника. Эта схема — итог такой проверки: общая ошибка и/или
    подробный журнал расхождений.

    Когда применять: чтобы получить результат завершённой проверки метаданных и решить,
    безопасен ли импорт. Записи журнала разнородны и вложены, поэтому представлены как
    «сырые» словари (``list[dict[str, Any]]``); каждая запись типично содержит тип
    (``type``: ``error``/``warning``/…), категорию и тексты объекта/значений/различий.

    Attributes:
        error_message: Общее сообщение об ошибке проверки; ``None``, если ошибок нет.
        check_metadata_errors: Журнал расхождений метаданных (сырые записи лога). Пустой
            список означает отсутствие расхождений.
    """

    error_message: str | None = Field(
        default=None, description="Общее сообщение об ошибке проверки"
    )
    check_metadata_errors: Annotated[list[dict[str, Any]], EmptyListIfNone] = Field(
        default_factory=list, description="Журнал расхождений метаданных (сырые записи)"
    )
