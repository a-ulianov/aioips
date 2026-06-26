"""Методы раздела почтового агента IPS Web API."""

from .mail_agent_settings import MailAgentSettingsMixin
from .unread_mail import UnreadMailMixin


class MailAgentAPI(MailAgentSettingsMixin, UnreadMailMixin):
    """Объединяет методы раздела почтового агента.

    References:
        Эндпоинты ``/core/api/MailAgent/*`` IPS Server Web API.
    """


__all__ = ["MailAgentAPI"]
