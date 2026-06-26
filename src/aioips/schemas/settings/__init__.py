"""Схемы раздела настроек (settings) IPS Web API."""

from .security_groups import ToolSecurityGroup, ToolSecurityRights
from .user_security_data import UserSecurityData
from .view_object_type_settings import ViewObjectTypeSettings

__all__ = [
    "ToolSecurityGroup",
    "ToolSecurityRights",
    "UserSecurityData",
    "ViewObjectTypeSettings",
]
