"""Методы раздела авторизации IPS Web API (``/core/api/Auth/*``)."""

from .authenticate import AuthenticateMixin
from .clone_tokens import CloneTokensMixin
from .login_options import LoginOptionsMixin
from .refresh_tokens import RefreshTokensMixin


class AuthAPI(LoginOptionsMixin, AuthenticateMixin, RefreshTokensMixin, CloneTokensMixin):
    """Сводный mixin раздела авторизации IPS.

    Собирает все методы-обёртки раздела ``Auth`` множественным наследованием
    и подмешивается в :class:`IPSClient`. На текущий момент предоставляет:

    - :meth:`~aioips.methods.auth.login_options.LoginOptionsMixin.login_options` —
      доступные роли и уровни доступа логина (без пароля), шаг до аутентификации.

    Сам жизненный цикл токена (authenticate / refresh) реализует ``AuthManager``
    в ядре клиента и здесь не дублируется.

    References:
        Эндпоинты ``/core/api/Auth/*`` IPS Server Web API. Домен: [[auth]].
    """


__all__ = ["AuthAPI"]
