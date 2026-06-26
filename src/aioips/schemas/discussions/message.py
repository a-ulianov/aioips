"""Схемы сообщения обсуждения объекта IPS.

Обсуждение (discussion) — поток сообщений, привязанный к ВЕРСИИ объекта IPS.
Каждое сообщение само является версионируемой сущностью со своим
идентификатором версии (``discussionVersionId``). Имена ключей JSON приходят
в ``camelCase`` без заглавных суффиксов-акронимов, поэтому явные алиасы не нужны —
сопоставление выполняет генератор ``to_camel`` базовой модели.

References:
    ``GET /core/api/discussions/getMessages`` — ``list[MessageDto]``.
    ``GET /core/api/discussions/{discussionVersionId}/getMessagesById`` —
    ``list[MessageDto]``.
    ``GET /core/api/discussions/{objectVersionId}/findMessages`` —
    ``list[MessageDto]``.
"""

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class MessageId(IPSModel):
    """Идентичность сообщения обсуждения (``MessageIdDto``).

    Составной идентификатор сообщения: версия записи сообщения
    (``discussion_version_id``), момент создания и версия-GUID автора. Именно
    ``discussion_version_id`` передаётся в :meth:`get_messages_by_id` для выборки
    сообщений конкретного обсуждения.

    Все три поля обязательны (свагер: ``required``).

    Attributes:
        discussion_version_id: Идентификатор ВЕРСИИ обсуждения/сообщения
            (``discussionVersionId``); ключ для :meth:`get_messages_by_id`.
        creation_timestamp: Момент создания сообщения (UTC).
        author_version_guid: GUID версии пользователя-автора сообщения.
    """

    discussion_version_id: int = Field(description="Идентификатор версии обсуждения/сообщения")
    creation_timestamp: datetime = Field(description="Момент создания сообщения (UTC)")
    author_version_guid: UUID = Field(description="GUID версии автора сообщения")


class GuidStringTuple(IPSModel):
    """Пара «GUID версии объекта → заголовок» (``GuidStringTuple``).

    Элемент карты контекста сообщения: сопоставляет GUID версии объекта его
    отображаемому заголовку. Заголовок (``item2``) может отсутствовать (``None``).

    Attributes:
        item1: GUID версии объекта.
        item2: Отображаемый заголовок объекта (может быть ``None``).
    """

    item1: UUID = Field(description="GUID версии объекта")
    item2: str | None = Field(default=None, description="Заголовок объекта")


class MessageContext(IPSModel):
    """Контекст сообщения обсуждения (``MessageContextDto``).

    Связывает сообщение с объектами, упомянутыми в нём: карта «GUID версии
    объекта → заголовок». Используется для разрешения ссылок на объекты при
    отображении текста сообщения.

    Attributes:
        object_version_guid_to_caption_map: Список пар «GUID версии объекта →
            заголовок» (``GuidStringTuple``); может быть пустым.
    """

    object_version_guid_to_caption_map: Annotated[list[GuidStringTuple], EmptyListIfNone] = Field(
        default_factory=list,
        description="Карта «GUID версии объекта → заголовок»",
    )


class Message(IPSModel):
    """Сообщение обсуждения, привязанного к версии объекта (``MessageDto``).

    Единица переписки в обсуждении объекта: автор, заголовок, текст, контекст
    упомянутых объектов и флаги доступности для ответа/правки. Возвращается
    методами чтения раздела discussions (:meth:`get_messages`,
    :meth:`get_messages_by_id`, :meth:`find_messages`).

    Идентичность сообщения — во вложенном :class:`MessageId` (поле ``id``), откуда
    берётся ``discussion_version_id`` для адресной выборки через
    :meth:`get_messages_by_id`.

    Обязательны (свагер: ``required``) поля ``id``, ``author_name``, ``caption``,
    ``context`` и ``text``; прочие необязательны с дефолтами — устойчиво к различиям
    ответов и версий API.

    Attributes:
        id: Идентичность сообщения (:class:`MessageId`), включая
            ``discussion_version_id``.
        author_name: Отображаемое имя автора сообщения.
        caption: Заголовок (тема) сообщения.
        last_modification_timestamp: Момент последнего изменения сообщения (UTC);
            ``None``, если сообщение не редактировалось.
        text: Текст сообщения.
        curious_users: GUID пользователей, отслеживающих сообщение/обсуждение;
            может быть пустым.
        context: Контекст упомянутых объектов (:class:`MessageContext`).
        is_read_only: Сообщение доступно только для чтения (правка запрещена).
        is_reply_only: На сообщение можно только отвечать (нельзя редактировать).
    """

    id: MessageId = Field(description="Идентичность сообщения")
    author_name: str = Field(description="Имя автора сообщения")
    caption: str = Field(description="Заголовок (тема) сообщения")
    last_modification_timestamp: datetime | None = Field(
        default=None, description="Момент последнего изменения сообщения (UTC)"
    )
    text: str = Field(description="Текст сообщения")
    curious_users: Annotated[list[UUID], EmptyListIfNone] = Field(
        default_factory=list, description="GUID пользователей, отслеживающих сообщение"
    )
    context: MessageContext = Field(description="Контекст упомянутых объектов")
    is_read_only: bool = Field(default=False, description="Сообщение только для чтения")
    is_reply_only: bool = Field(default=False, description="На сообщение можно только отвечать")
