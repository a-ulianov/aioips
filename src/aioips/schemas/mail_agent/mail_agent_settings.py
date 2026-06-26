"""Схема настроек почтового агента IPS.

References:
    ``GET /core/api/MailAgent/settings`` — ``MailAgentSettingsDTO``.
"""

from pydantic import Field

from ..base import IPSModel
from .unread_mail_settings import UnreadMailSettings


class MailAgentSettings(IPSModel):
    """Настройки почтового агента IPS.

    Возвращается методом получения настроек почтового агента и агрегирует группы
    параметров его работы. На текущей версии API содержит настройки проверки
    непрочитанной почты (:class:`UnreadMailSettings`).

    Attributes:
        unread_mail: Настройки периодической проверки непрочитанной почты.
    """

    unread_mail: UnreadMailSettings = Field(
        description="Настройки периодической проверки непрочитанной почты"
    )
