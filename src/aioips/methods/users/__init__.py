"""Методы раздела пользователей IPS Web API (``/core/api/currentUsers/*``)."""

from .id_helper import IdHelperMixin
from .user_info import UserInfoMixin


class UsersAPI(UserInfoMixin, IdHelperMixin):
    """Сводный mixin раздела пользователей IPS.

    Собирает методы-обёртки раздела ``currentUsers`` множественным наследованием
    и подмешивается в :class:`IPSClient`. На текущий момент предоставляет:

    - :meth:`~aioips.methods.users.user_info.UserInfoMixin.user_info` —
      сведения о пользователе текущей сессии (роль, уровень доступа, ``is_admin``).

    References:
        Эндпоинты ``/core/api/currentUsers/*`` IPS Server Web API. Домен: [[auth]].
    """


__all__ = ["UsersAPI"]
