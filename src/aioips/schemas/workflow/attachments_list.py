"""Схемы вложений активности процесса IPS.

References:
    ``GET /core/api/wfAttachments/{activityId}/getAttachmments`` — ``AttachmentsListDTO``
    (элемент массива ``attachments`` — ``AttachmentDTO``).
"""

from typing import Annotated

from pydantic import Field

from ...common.enumerations import ObjectModifyMode
from ..base import EmptyListIfNone, IPSModel


class Attachment(IPSModel):
    """Объект, прикреплённый к активности (задаче) процесса как вложение.

    Вложение активности workflow — это объект IPS (документ/версия), привязанный к
    шагу процесса. DTO описывает идентичность объекта-вложения и сведения,
    необходимые для отображения и проверки прав на правку (тип, владелец, состояние
    извлечения и допустимый режим изменения).

    Предусловие по id-пространству: ``object_id`` — это идентификатор ОБЪЕКТА
    (``objectID`` / F_OBJECT_ID), а не идентификатор версии. По нему объект
    загружается через :meth:`object_get`.

    Attributes:
        object_id: Идентификатор ОБЪЕКТА-вложения (``objectID`` / F_OBJECT_ID).
        object_type: Числовой идентификатор типа объекта-вложения.
        caption: Заголовок объекта-вложения.
        owner_id: Идентификатор владельца объекта-вложения.
        object_type_name: Наименование типа объекта (может отсутствовать).
        owner_name: Имя владельца объекта (может отсутствовать).
        check_out_by: Идентификатор пользователя, извлёкшего объект (0 — не извлечён).
        object_modify_mode: Режим, в котором допускается правка объекта
            (:class:`ObjectModifyMode`); определяет необходимость цикла checkout.
    """

    object_id: int = Field(description="Идентификатор ОБЪЕКТА-вложения (objectID)")
    object_type: int = Field(description="Идентификатор типа объекта-вложения")
    caption: str = Field(description="Заголовок объекта-вложения")
    owner_id: int = Field(description="Идентификатор владельца объекта-вложения")
    object_type_name: str | None = Field(default=None, description="Наименование типа объекта")
    owner_name: str | None = Field(default=None, description="Имя владельца объекта")
    check_out_by: int = Field(
        default=0, description="Идентификатор пользователя, извлёкшего объект (0 — не извлечён)"
    )
    object_modify_mode: ObjectModifyMode | None = Field(
        default=None, description="Режим, в котором допускается правка объекта"
    )


class AttachmentsList(IPSModel):
    """Список вложений активности процесса с признаком наличия скрытых элементов.

    Возвращается методом :meth:`wf_attachments`. Содержит видимые текущему
    пользователю вложения и флаг, сигнализирующий, что часть вложений скрыта
    (например, недоступна по правам), — учитывайте его, чтобы не считать список
    исчерпывающим.

    Attributes:
        attachments: Список вложений активности (см. :class:`Attachment`); пустой,
            если у активности нет видимых вложений.
        has_invisible_items: Признак наличия невидимых текущему пользователю вложений
            (``True`` — список неполный из-за скрытых элементов).
    """

    attachments: Annotated[list[Attachment], EmptyListIfNone] = Field(
        default_factory=list, description="Список вложений активности процесса"
    )
    has_invisible_items: bool = Field(
        default=False, description="Признак наличия невидимых текущему пользователю вложений"
    )
