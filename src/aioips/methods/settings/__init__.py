"""Методы раздела настроек (settings) IPS Web API."""

from .add_or_update_security_data import AddOrUpdateSecurityDataMixin
from .remove_security_data import RemoveSecurityDataMixin
from .security_data import SecurityDataMixin
from .set_view_print_settings import SetViewPrintSettingsMixin
from .user_group import UserGroupMixin
from .user_rights import UserRightsMixin
from .view_print_settings import ViewPrintSettingsMixin


class SettingsAPI(
    SecurityDataMixin,
    UserGroupMixin,
    UserRightsMixin,
    ViewPrintSettingsMixin,
    SetViewPrintSettingsMixin,
    AddOrUpdateSecurityDataMixin,
    RemoveSecurityDataMixin,
):
    """Объединяет методы раздела настроек (settings).

    References:
        Эндпоинты ``/core/api/settings/*`` IPS Server Web API.
    """


__all__ = ["SettingsAPI"]
