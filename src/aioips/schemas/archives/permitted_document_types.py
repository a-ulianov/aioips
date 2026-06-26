"""Схема допустимых типов документов архива IPS.

References:
    ``POST /core/api/archives/{archiveId}/canApplySettings`` — тело запроса
    ``PermittedDocumentTypesDto``.
"""

from typing import Annotated

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class PermittedDocumentTypes(IPSModel):
    """Допустимые типы документов архива (``PermittedDocumentTypesDto``).

    Тело запроса для метода :meth:`archive_can_apply_settings`. Описывает набор типов
    документов (``documents_types``) и режим их применения (``types_using_mode``) для
    проверки применимости настроек к архиву. Несмотря на HTTP-метод POST, метод-получатель
    выполняет ЧТЕНИЕ/ПРОВЕРКУ — сервер ничего не изменяет, лишь сообщает, можно ли применить
    такие настройки.

    Сериализуйте тело как ``model_dump(mode="json", by_alias=True, exclude_none=True)``.

    Attributes:
        documents_types: Идентификаторы ТИПОВ документов (``documentsTypes``, list[int],
            id-пространство типов объектов), охватываемых настройкой; ``null``
            нормализуется в пустой список. По умолчанию пустой список.
        types_using_mode: Режим применения перечня типов (``typesUsingMode``, строка;
            например «белый»/«чёрный» список — точные значения задаёт сервер).
            По умолчанию ``""``.
    """

    documents_types: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list,
        alias="documentsTypes",
        description="Идентификаторы типов документов",
    )
    types_using_mode: str = Field(
        default="",
        alias="typesUsingMode",
        description="Режим применения перечня типов",
    )
