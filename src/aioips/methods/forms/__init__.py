"""Методы раздела форм (forms) IPS Web API."""

from .default_columns_for_widget import DefaultColumnsForWidgetMixin
from .default_widget_colors import DefaultWidgetColorsMixin
from .find_applicability import FindApplicabilityMixin
from .find_collection import FindCollectionMixin
from .find_composition import FindCompositionMixin
from .find_objects_list import FindObjectsListMixin
from .find_user_groups_and_users import FindUserGroupsAndUsersMixin
from .find_user_groups_and_users_in_composition import (
    FindUserGroupsAndUsersInCompositionMixin,
)
from .find_user_groups_in_composition import FindUserGroupsInCompositionMixin
from .find_users import FindUsersMixin
from .form import FormMixin
from .form_related_object_type_guids import FormRelatedObjectTypeGuidsMixin
from .form_related_relation_type_guids import FormRelatedRelationTypeGuidsMixin
from .forms_for import FormsForMixin
from .image_for_widget import ImageForWidgetMixin
from .rank_find_collection import RankFindCollectionMixin
from .rank_find_inner_users import RankFindInnerUsersMixin
from .save_form_widget import SaveFormWidgetMixin
from .subject_area_find_collection import SubjectAreaFindCollectionMixin
from .system_colors import SystemColorsMixin
from .user_find_collection import UserFindCollectionMixin
from .user_group_find_collection import UserGroupFindCollectionMixin
from .user_group_find_roots import UserGroupFindRootsMixin
from .widget_colors import WidgetColorsMixin


class FormsAPI(
    FindUserGroupsInCompositionMixin,
    RankFindInnerUsersMixin,
    FindUserGroupsAndUsersMixin,
    WidgetColorsMixin,
    SystemColorsMixin,
    FindUserGroupsAndUsersInCompositionMixin,
    UserGroupFindRootsMixin,
    DefaultColumnsForWidgetMixin,
    DefaultWidgetColorsMixin,
    ImageForWidgetMixin,
    SubjectAreaFindCollectionMixin,
    FormMixin,
    FormsForMixin,
    FormRelatedObjectTypeGuidsMixin,
    FormRelatedRelationTypeGuidsMixin,
    FindApplicabilityMixin,
    FindCollectionMixin,
    FindCompositionMixin,
    FindObjectsListMixin,
    FindUsersMixin,
    RankFindCollectionMixin,
    UserFindCollectionMixin,
    UserGroupFindCollectionMixin,
    SaveFormWidgetMixin,
):
    """Объединяет методы чтения раздела форм.

    References:
        Эндпоинты ``/core/api/forms/*`` IPS Server Web API.
    """


__all__ = ["FormsAPI"]
