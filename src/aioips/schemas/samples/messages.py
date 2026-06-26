"""Схемы демонстрационного раздела сообщений (samples/messages)."""

from datetime import datetime

from pydantic import Field

from ..base import IPSModel


class AddMessage(IPSModel):
    """Тело запроса на добавление демо-сообщения (``AddMessageDTO``).

    Назначение: типизированная форма полезной нагрузки :meth:`add_message`. Раздел
    ``samples`` — учебный (демо-API сообщений/уведомлений), на доменные объекты IPS
    не влияет; служит для проверки соединения и примеров клиента.

    Поля:
        id: Идентификатор сообщения. ``0`` означает, что сервер присвоит идентификатор
            автоматически (рекомендуемое значение при добавлении нового сообщения).
        text: Текст сообщения.

    Notes:
        operationId ``Messages_Add``. Сериализуйте в тело запроса через
        ``model_dump(by_alias=True)``.
    """

    id: int = Field(default=0, ge=0)
    text: str


class FullMessage(IPSModel):
    """Полное представление демо-сообщения (``FullMessageDTO``).

    Назначение: типизированный разбор ответов чтений/мутаций раздела (например
    :meth:`message_by_id`, :meth:`add_message`) и тело запроса :meth:`update_message`.

    Поля:
        id: Уникальный идентификатор сообщения (>= 1).
        create_time: Дата создания сообщения (UTC, ``date-time``).
        last_write_time: Дата последнего изменения сообщения (UTC, ``date-time``).
        text: Текст сообщения.

    Notes:
        Возвращается операциями ``Messages_GetAll`` / ``Messages_GetById`` /
        ``Messages_Add`` / ``Messages_Update`` / ``Messages_UpdateText`` /
        ``Messages_UpdateLastWriteTime``.
    """

    id: int = Field(ge=1)
    create_time: datetime
    last_write_time: datetime
    text: str
