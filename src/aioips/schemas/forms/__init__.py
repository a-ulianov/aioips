"""Схемы раздела форм (forms) IPS Web API."""

from .find_collection_options import FindCollectionOptions
from .form_object import FormObjectDto
from .ids_find_users_request import Ids4FindUsersRequest
from .subject_area import SubjectArea
from .user import User
from .user_group import UserGroup
from .user_group_and_user import UserGroupAndUser
from .version_id_and_columns_request import VersionIdAndColumns4Request
from .widget import Widget
from .widget_color import WidgetColor
from .widget_grid_column import WidgetGridColumn

__all__ = [
    "FindCollectionOptions",
    "FormObjectDto",
    "Ids4FindUsersRequest",
    "SubjectArea",
    "User",
    "UserGroup",
    "UserGroupAndUser",
    "VersionIdAndColumns4Request",
    "Widget",
    "WidgetColor",
    "WidgetGridColumn",
]
