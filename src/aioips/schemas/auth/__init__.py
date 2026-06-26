"""Схемы раздела авторизации IPS Web API (``/core/api/Auth/*``).

Экспортирует DTO опций входа: :class:`AuthOptions` (агрегат) и его элементы
:class:`AuthRole`, :class:`AuthAccessLevel`. Домен: разделу авторизации.
"""

from .login_options import AuthAccessLevel, AuthOptions, AuthRole

__all__ = ["AuthAccessLevel", "AuthOptions", "AuthRole"]
