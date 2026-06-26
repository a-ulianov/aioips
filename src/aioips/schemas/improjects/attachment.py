"""Схема вложения задачи проекта IPS (Improject).

References:
    ``GET /core/api/improjects/tasks/{taskId}/attachments`` — массив ``AttachmentDto``.
"""

from pydantic import Field

from ..base import IPSModel


class Attachment(IPSModel):
    """Вложение задачи проекта Improject (ссылка на объект-вложение).

    Описывает один прикреплённый к задаче объект (исходные данные или результаты).
    Возвращается методом :meth:`task_attachments` списком. Вложение ссылается на
    объект IPS (``object_id``) — загрузить его целиком можно через
    :meth:`object_get` по ``object_id``.

    Предусловие по id-пространству: ``object_id`` — это идентификатор ОБЪЕКТА
    (``objectID`` / F_OBJECT_ID), пригодный для :meth:`object_get`; ``id`` —
    идентификатор записи вложения в контексте задачи, а не версия объекта.

    Все перечисленные поля обязательны по описанию API.

    Attributes:
        id: Идентификатор записи вложения.
        object_id: Идентификатор объекта-вложения (``objectID``) для :meth:`object_get`.
        type_id: Идентификатор типа объекта-вложения.
        object_type_name: Наименование типа объекта-вложения.
        caption: Заголовок (отображаемое имя) вложения.
        owner: Идентификатор владельца вложения.
        owner_name: Имя владельца вложения.
    """

    id: int = Field(description="Идентификатор записи вложения")
    object_id: int = Field(description="Идентификатор объекта-вложения (objectID)")
    type_id: int = Field(description="Идентификатор типа объекта-вложения")
    object_type_name: str = Field(description="Наименование типа объекта-вложения")
    caption: str = Field(description="Заголовок вложения")
    owner: int = Field(description="Идентификатор владельца вложения")
    owner_name: str = Field(description="Имя владельца вложения")
