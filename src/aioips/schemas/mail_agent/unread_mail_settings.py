"""Схема настроек проверки непрочитанной почты IPS.

References:
    Вложена в ``MailAgentSettingsDTO`` (поле ``unreadMail``) — ``UnreadMailSettingsDTO``.
"""

from pydantic import Field

from ..base import IPSModel


class UnreadMailSettings(IPSModel):
    """Настройки периодической проверки непрочитанной почты почтовым агентом IPS.

    Описывает, как часто почтовый агент опрашивает почтовый ящик на наличие новых
    (непрочитанных) писем. Является вложенной частью настроек почтового агента
    (:class:`MailAgentSettings`).

    Attributes:
        check_interval: Интервал проверки почты в минутах (по умолчанию 5). Значение
            ``<= 0`` отключает периодическую проверку (опрос не выполняется).
    """

    check_interval: int = Field(
        default=5,
        description="Интервал проверки почты в минутах (<= 0 отключает проверку)",
    )
