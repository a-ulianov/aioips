"""Схемы раздела почтового агента IPS Web API."""

from .mail_agent_settings import MailAgentSettings
from .unread_mail import UnreadMail
from .unread_mail_settings import UnreadMailSettings

__all__ = ["MailAgentSettings", "UnreadMail", "UnreadMailSettings"]
