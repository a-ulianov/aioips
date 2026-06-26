"""Схема запроса замены версии объекта в контексте редактирования.

References:
    ``POST /core/api/editingContexts/{editingContextId}/replace`` — тело
    ``ReplaceVersionInEditingContextDto``.
"""

from pydantic import Field

from ..base import IPSModel


class ReplaceVersionInEditingContext(IPSModel):
    """Тело запроса замены версии объекта в контексте редактирования.

    Заменяет одну версию объекта, уже состоящую в контексте редактирования, на
    другую версию. Оба идентификатора — это ``id`` ВЕРСИЙ объектов (F_ID), а не
    ``objectID`` объектов.

    Attributes:
        editing_context_version_id: Идентификатор версии объекта (``id`` / F_ID),
            находящейся в контексте и подлежащей замене. Обязательное поле.
        replacement_version_id: Идентификатор версии объекта (``id`` / F_ID), на
            которую выполняется замена. Обязательное поле.
    """

    editing_context_version_id: int = Field(
        description="Идентификатор версии объекта в контексте, подлежащей замене"
    )
    replacement_version_id: int = Field(
        description="Идентификатор версии объекта, на которую выполняется замена"
    )
