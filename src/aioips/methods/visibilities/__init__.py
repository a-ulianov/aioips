"""Методы раздела настроек видимости IPS Web API."""

from .default_visibility_settings import DefaultVisibilitySettingsMixin


class VisibilitiesAPI(DefaultVisibilitySettingsMixin):
    """Объединяет методы раздела настроек видимости.

    References:
        Эндпоинты ``/api/visibilities/*`` IPS Server Web API.
    """


__all__ = ["VisibilitiesAPI"]
