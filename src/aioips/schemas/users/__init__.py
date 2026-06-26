"""Схемы раздела пользователей IPS Web API (``/core/api/currentUsers/*``).

Экспортирует :class:`CurrentUserInfo` — DTO сведений о пользователе текущей
сессии. Домен: [[auth]].
"""

from .id_helper import IdHelper
from .user_info import CurrentUserInfo

__all__ = ["CurrentUserInfo", "IdHelper"]
