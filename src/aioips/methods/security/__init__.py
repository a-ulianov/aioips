"""Методы раздела прав доступа (безопасности) IPS Web API."""

from .actions_on_objects_security import ActionsOnObjectsSecurityMixin
from .attribute_group_security import AttributeGroupSecurityMixin
from .attribute_groups_security import AttributeGroupsSecurityMixin
from .attribute_security import AttributeSecurityMixin
from .attributes_collection_security import AttributesCollectionSecurityMixin
from .check_actions_on_objects_security_access import CheckActionsOnObjectsSecurityAccessMixin
from .check_attribute_group_security_access import CheckAttributeGroupSecurityAccessMixin
from .check_attribute_groups_security_access import CheckAttributeGroupsSecurityAccessMixin
from .check_attribute_security_access import CheckAttributeSecurityAccessMixin
from .check_attributes_security_access import CheckAttributesSecurityAccessMixin
from .check_languages_security_access import CheckLanguagesSecurityAccessMixin
from .check_lifecycle_level_security_access import CheckLifecycleLevelSecurityAccessMixin
from .check_lifecycle_levels_security_access import CheckLifecycleLevelsSecurityAccessMixin
from .check_lifecycle_scheme_security_access import CheckLifecycleSchemeSecurityAccessMixin
from .check_lifecycle_schemes_security_access import CheckLifecycleSchemesSecurityAccessMixin
from .check_object_security_access import CheckObjectSecurityAccessMixin
from .check_object_type_lifecycle_step_attribute_access import (
    CheckObjectTypeLifecycleSchemeStepAccessForAttributeMixin,
)
from .check_object_type_lifecycle_step_attribute_security_access import (
    CheckObjectTypeLifecycleStepAttributeSecurityAccessMixin,
)
from .check_object_type_lifecycle_step_security_access import (
    CheckObjectTypeLifecycleStepSecurityAccessMixin,
)
from .check_object_type_security_access import CheckObjectTypeSecurityAccessMixin
from .check_object_types_security_access import CheckObjectTypesSecurityAccessMixin
from .check_relation_type_security_access import CheckRelationTypeSecurityAccessMixin
from .check_relation_types_security_access import CheckRelationTypesSecurityAccessMixin
from .check_subject_areas_security_access import CheckSubjectAreasSecurityAccessMixin
from .check_system_security_access import CheckSystemSecurityAccessMixin
from .check_update_object_type_lifecycle_step_access import (
    CheckUpdateObjectTypeLifecycleSchemeStepAccessMixin,
)
from .languages_security import LanguagesSecurityMixin
from .lifecycle_level_security import LifecycleLevelSecurityMixin
from .lifecycle_levels_security import LifecycleLevelsSecurityMixin
from .lifecycle_scheme_security import LifecycleSchemeSecurityMixin
from .lifecycle_schemes_security import LifecycleSchemesSecurityMixin
from .object_security import ObjectSecurityMixin
from .object_type_lifecycle_step_attribute_security import (
    ObjectTypeLifecycleStepAttributeSecurityMixin,
)
from .object_type_lifecycle_step_security import ObjectTypeLifecycleStepSecurityMixin
from .object_type_security import ObjectTypeSecurityMixin
from .object_types_security import ObjectTypesSecurityMixin
from .relation_type_security import RelationTypeSecurityMixin
from .relation_types_security import RelationTypesSecurityMixin
from .restore_admin_access_actions_on_objects import RestoreAdminAccessActionsOnObjectsMixin
from .restore_admin_access_attribute import RestoreAdminAccessAttributeMixin
from .restore_admin_access_attribute_group import RestoreAdminAccessAttributeGroupMixin
from .restore_admin_access_attribute_groups import RestoreAdminAccessAttributeGroupsMixin
from .restore_admin_access_attributes import RestoreAdminAccessAttributesMixin
from .restore_admin_access_languages import RestoreAdminAccessLanguagesMixin
from .restore_admin_access_lifecycle_level import RestoreAdminAccessLifecycleLevelMixin
from .restore_admin_access_lifecycle_levels import RestoreAdminAccessLifecycleLevelsMixin
from .restore_admin_access_lifecycle_scheme import RestoreAdminAccessLifecycleSchemeMixin
from .restore_admin_access_lifecycle_schemes import RestoreAdminAccessLifecycleSchemesMixin
from .restore_admin_access_object import RestoreAdminAccessObjectMixin
from .restore_admin_access_object_type import RestoreAdminAccessObjectTypeMixin
from .restore_admin_access_object_type_lifecycle_scheme_step import (
    RestoreAdminAccessObjectTypeLifecycleSchemeStepMixin,
)
from .restore_admin_access_object_types import RestoreAdminAccessObjectTypesMixin
from .restore_admin_access_relation_type import RestoreAdminAccessRelationTypeMixin
from .restore_admin_access_relation_types import RestoreAdminAccessRelationTypesMixin
from .restore_admin_access_subject_areas import RestoreAdminAccessSubjectAreasMixin
from .restore_admin_access_system import RestoreAdminAccessSystemMixin
from .restore_object_type_lifecycle_scheme_step_for_attribute import (
    RestoreObjectTypeLifecycleSchemeStepForAttributeMixin,
)
from .subject_areas_security import SubjectAreasSecurityMixin
from .system_security import SystemSecurityMixin
from .update_object_type_lifecycle_step_attribute_security import (
    UpdateObjectTypeLifecycleSchemeStepSecurityForAttributeMixin,
)
from .update_object_type_lifecycle_step_child_targets import (
    UpdateObjectTypeLifecycleSchemeStepChildTargetsMixin,
)
from .update_object_type_lifecycle_step_security import (
    UpdateObjectTypeLifecycleSchemeStepSecurityMixin,
)
from .update_object_type_security_child_targets import UpdateObjectTypeSecurityChildTargetsMixin


class SecurityAPI(
    ObjectSecurityMixin,
    ObjectTypeSecurityMixin,
    ObjectTypesSecurityMixin,
    AttributeSecurityMixin,
    ActionsOnObjectsSecurityMixin,
    SystemSecurityMixin,
    SubjectAreasSecurityMixin,
    LanguagesSecurityMixin,
    AttributesCollectionSecurityMixin,
    AttributeGroupsSecurityMixin,
    AttributeGroupSecurityMixin,
    RelationTypesSecurityMixin,
    RelationTypeSecurityMixin,
    LifecycleLevelsSecurityMixin,
    LifecycleLevelSecurityMixin,
    LifecycleSchemesSecurityMixin,
    LifecycleSchemeSecurityMixin,
    ObjectTypeLifecycleStepSecurityMixin,
    ObjectTypeLifecycleStepAttributeSecurityMixin,
    # checkAccess — read-only проверки прав текущего пользователя
    CheckActionsOnObjectsSecurityAccessMixin,
    CheckAttributeGroupsSecurityAccessMixin,
    CheckAttributeGroupSecurityAccessMixin,
    CheckAttributesSecurityAccessMixin,
    CheckAttributeSecurityAccessMixin,
    CheckLanguagesSecurityAccessMixin,
    CheckLifecycleLevelsSecurityAccessMixin,
    CheckLifecycleLevelSecurityAccessMixin,
    CheckLifecycleSchemesSecurityAccessMixin,
    CheckLifecycleSchemeSecurityAccessMixin,
    CheckObjectTypesSecurityAccessMixin,
    CheckObjectTypeSecurityAccessMixin,
    CheckObjectTypeLifecycleStepSecurityAccessMixin,
    CheckObjectTypeLifecycleStepAttributeSecurityAccessMixin,
    CheckObjectSecurityAccessMixin,
    CheckRelationTypesSecurityAccessMixin,
    CheckRelationTypeSecurityAccessMixin,
    CheckSubjectAreasSecurityAccessMixin,
    CheckSystemSecurityAccessMixin,
    CheckObjectTypeLifecycleSchemeStepAccessForAttributeMixin,
    CheckUpdateObjectTypeLifecycleSchemeStepAccessMixin,
    # restoreAdminAccess — восстановление доступа администратора (мутации, confirm)
    RestoreAdminAccessActionsOnObjectsMixin,
    RestoreAdminAccessAttributeGroupsMixin,
    RestoreAdminAccessAttributeGroupMixin,
    RestoreAdminAccessAttributesMixin,
    RestoreAdminAccessAttributeMixin,
    RestoreAdminAccessLanguagesMixin,
    RestoreAdminAccessLifecycleLevelsMixin,
    RestoreAdminAccessLifecycleLevelMixin,
    RestoreAdminAccessLifecycleSchemesMixin,
    RestoreAdminAccessLifecycleSchemeMixin,
    RestoreAdminAccessObjectTypesMixin,
    RestoreAdminAccessObjectTypeMixin,
    RestoreAdminAccessObjectTypeLifecycleSchemeStepMixin,
    RestoreObjectTypeLifecycleSchemeStepForAttributeMixin,
    RestoreAdminAccessObjectMixin,
    RestoreAdminAccessRelationTypesMixin,
    RestoreAdminAccessRelationTypeMixin,
    RestoreAdminAccessSubjectAreasMixin,
    RestoreAdminAccessSystemMixin,
    # update*/childTargets — установка прав (мутации, confirm)
    UpdateObjectTypeSecurityChildTargetsMixin,
    UpdateObjectTypeLifecycleSchemeStepSecurityMixin,
    UpdateObjectTypeLifecycleSchemeStepSecurityForAttributeMixin,
    UpdateObjectTypeLifecycleSchemeStepChildTargetsMixin,
):
    """Объединяет методы чтения прав доступа (безопасности).

    Все методы — read-only: возвращают снимок прав :class:`Security` (кто какие
    действия может выполнять над объектом, типом, атрибутом или операциями над
    объектами). Изменение прав в данной версии не реализовано.

    References:
        Эндпоинты ``/core/api/security/*`` IPS Server Web API.
    """


__all__ = ["SecurityAPI"]
