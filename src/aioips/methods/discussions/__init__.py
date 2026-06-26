"""Методы раздела обсуждений (discussions) IPS Web API."""

from .add_discussion_image import AddDiscussionImageMixin
from .add_message import AddMessageMixin
from .can_discuss import CanDiscussMixin
from .edit_message import EditMessageMixin
from .find_messages import FindMessagesMixin
from .get_messages import GetMessagesMixin
from .get_messages_by_id import GetMessagesByIdMixin
from .remove_message import RemoveMessageMixin


class DiscussionsAPI(
    CanDiscussMixin,
    GetMessagesMixin,
    GetMessagesByIdMixin,
    FindMessagesMixin,
    AddMessageMixin,
    EditMessageMixin,
    RemoveMessageMixin,
    AddDiscussionImageMixin,
):
    """Объединяет методы чтения раздела обсуждений.

    References:
        Эндпоинты ``/core/api/discussions/*`` IPS Server Web API.
    """


__all__ = ["DiscussionsAPI"]
