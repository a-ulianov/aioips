"""Методы демонстрационного раздела (samples) IPS Web API."""

from .add_message import AddMessageSampleMixin
from .clear_message_updates import ClearMessageUpdatesMixin
from .delete_message import DeleteMessageMixin
from .message_by_id import MessageByIdMixin
from .messages import MessagesMixin
from .messages_by_filter import MessagesByFilterMixin
from .sample_value_as_content import SampleValueAsContentMixin
from .sample_value_as_file import SampleValueAsFileMixin
from .sample_value_as_long import SampleValueAsLongMixin
from .sample_values import SampleValuesMixin
from .update_message import UpdateMessageMixin
from .update_message_last_write_time import UpdateMessageLastWriteTimeMixin
from .update_message_text import UpdateMessageTextMixin


class SamplesAPI(
    MessagesMixin,
    MessageByIdMixin,
    MessagesByFilterMixin,
    SampleValuesMixin,
    AddMessageSampleMixin,
    ClearMessageUpdatesMixin,
    UpdateMessageMixin,
    DeleteMessageMixin,
    UpdateMessageLastWriteTimeMixin,
    UpdateMessageTextMixin,
    SampleValueAsContentMixin,
    SampleValueAsFileMixin,
    SampleValueAsLongMixin,
):
    """Объединяет методы демонстрационного (учебного) раздела ``samples``.

    Раздел не затрагивает доменные объекты IPS: демо-API сообщений/уведомлений
    (чтения и CRUD) и приветствие пользователя. Применяется для проверки
    соединения/авторизации и как пример работы клиента.

    References:
        Эндпоинты ``/core/api/samples/*`` IPS Server Web API.
    """


__all__ = ["SamplesAPI"]
