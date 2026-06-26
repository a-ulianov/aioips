"""Методы раздела объектов IPS Web API."""

from .object_add_objects_by_template import ObjectAddObjectsByTemplateMixin
from .object_add_temporary_attribute import ObjectAddTemporaryAttributeMixin
from .object_attribute import ObjectAttributeMixin
from .object_attribute_as_string import ObjectAttributeAsStringMixin
from .object_attribute_descriptions import ObjectAttributeDescriptionsMixin
from .object_attribute_values import ObjectAttributeValuesMixin
from .object_attribute_values_by_guid import ObjectAttributeValuesByGuidMixin
from .object_attributes import ObjectAttributesMixin
from .object_attributes_descriptions import ObjectAttributesDescriptionsMixin
from .object_attributes_init_values import ObjectAttributesInitValuesMixin
from .object_attributes_values import ObjectAttributesValuesMixin
from .object_base_version import ObjectBaseVersionMixin
from .object_by_version_rule import ObjectByVersionRuleMixin
from .object_by_version_rule_by_guid import ObjectByVersionRuleByGuidMixin
from .object_by_versions_rule import ObjectByVersionsRuleMixin
from .object_calculated_attribute_values import ObjectCalculatedAttributeValuesMixin
from .object_can_set_next_lc_step import ObjectCanSetNextLcStepMixin
from .object_cancel_changes import ObjectCancelChangesMixin
from .object_check_access_rights_for_visibility import (
    ObjectCheckAccessRightsForVisibilityMixin,
)
from .object_check_edit import ObjectCheckEditMixin
from .object_check_in import ObjectCheckInMixin
from .object_check_in_command import ObjectCheckInCommandMixin
from .object_check_out import ObjectCheckOutMixin
from .object_check_out_versions import ObjectCheckOutVersionsMixin
from .object_check_out_with_check_modify import ObjectCheckOutWithCheckModifyMixin
from .object_check_relations_edit import ObjectCheckRelationsEditMixin
from .object_check_visibility_available import ObjectCheckVisibilityAvailableMixin
from .object_checkout_date import ObjectCheckoutDateMixin
from .object_cleanup_attribute import ObjectCleanupAttributeMixin
from .object_commit_creation import ObjectCommitCreationMixin
from .object_composition import ObjectCompositionMixin
from .object_composition_with_params import ObjectCompositionWithParamsMixin
from .object_connect_to_object import ObjectConnectToObjectMixin
from .object_create import ObjectCreateMixin
from .object_create_by_prototype import ObjectCreateByPrototypeMixin
from .object_create_object_version import ObjectCreateObjectVersionMixin
from .object_delete import ObjectDeleteMixin
from .object_delete_attribute import ObjectDeleteAttributeMixin
from .object_edit import ObjectEditMixin
from .object_exclude_from_composition import ObjectExcludeFromCompositionMixin
from .object_get import ObjectGetMixin
from .object_get_by_guid import ObjectGetByGuidMixin
from .object_hash_version import ObjectHashVersionMixin
from .object_include_in_composition import ObjectIncludeInCompositionMixin
from .object_info import ObjectInfoMixin
from .object_info_by_guid import ObjectInfoByGuidMixin
from .object_is_parent_type import ObjectIsParentTypeMixin
from .object_load_descriptions import ObjectLoadDescriptionsMixin
from .object_make_base_version import ObjectMakeBaseVersionMixin
from .object_make_base_versions import ObjectMakeBaseVersionsMixin
from .object_print import ObjectPrintMixin
from .object_rollback_check_out import ObjectRollbackCheckOutMixin
from .object_save_changes import ObjectSaveChangesMixin
from .object_save_to_arc_copy import ObjectSaveToArcCopyMixin
from .object_save_to_disk import ObjectSaveToDiskMixin
from .object_set_attribute_values import ObjectSetAttributeValuesMixin
from .object_set_attribute_values_ex import ObjectSetAttributeValuesExMixin
from .object_set_attributes import ObjectSetAttributesMixin
from .object_set_modify_content_date import ObjectSetModifyContentDateMixin
from .object_snapshot_info import ObjectSnapshotInfoMixin
from .object_snapshot_readonly_objects import ObjectSnapshotReadonlyObjectsMixin
from .object_update_visibility_settings import ObjectUpdateVisibilitySettingsMixin
from .object_validate_set_next_lc_step import ObjectValidateSetNextLcStepMixin
from .object_visibilities import ObjectVisibilitiesMixin
from .objects_all_versions import ObjectsAllVersionsMixin
from .objects_collection import ObjectsCollectionMixin
from .objects_select import ObjectsSelectMixin
from .objects_select_iter import ObjectsSelectIterMixin
from .objects_select_request import ObjectsSelectByIdMixin, ObjectsSelectRequestMixin


class ObjectsAPI(
    ObjectGetMixin,
    ObjectGetByGuidMixin,
    ObjectInfoMixin,
    ObjectInfoByGuidMixin,
    ObjectsCollectionMixin,
    ObjectsSelectIterMixin,
    ObjectsSelectMixin,
    ObjectAttributesMixin,
    ObjectAttributeMixin,
    ObjectAttributeValuesMixin,
    ObjectAttributesValuesMixin,
    ObjectAttributesDescriptionsMixin,
    ObjectAttributeDescriptionsMixin,
    ObjectAttributeAsStringMixin,
    ObjectAttributesInitValuesMixin,
    ObjectBaseVersionMixin,
    ObjectCompositionWithParamsMixin,
    ObjectSetAttributeValuesMixin,
    ObjectSetAttributesMixin,
    ObjectDeleteAttributeMixin,
    ObjectCleanupAttributeMixin,
    ObjectAddTemporaryAttributeMixin,
    ObjectCreateMixin,
    ObjectCommitCreationMixin,
    ObjectCheckOutMixin,
    ObjectCheckInMixin,
    ObjectSaveChangesMixin,
    ObjectDeleteMixin,
    ObjectsAllVersionsMixin,
    ObjectCompositionMixin,
    ObjectByVersionsRuleMixin,
    ObjectCalculatedAttributeValuesMixin,
    ObjectCreateObjectVersionMixin,
    ObjectEditMixin,
    ObjectCancelChangesMixin,
    ObjectIncludeInCompositionMixin,
    ObjectMakeBaseVersionsMixin,
    ObjectMakeBaseVersionMixin,
    ObjectConnectToObjectMixin,
    ObjectCheckInCommandMixin,
    ObjectValidateSetNextLcStepMixin,
    ObjectCreateByPrototypeMixin,
    ObjectExcludeFromCompositionMixin,
    ObjectSetAttributeValuesExMixin,
    ObjectAddObjectsByTemplateMixin,
    ObjectCheckOutWithCheckModifyMixin,
    ObjectCanSetNextLcStepMixin,
    ObjectCheckoutDateMixin,
    ObjectHashVersionMixin,
    ObjectIsParentTypeMixin,
    ObjectByVersionRuleMixin,
    ObjectByVersionRuleByGuidMixin,
    ObjectCheckRelationsEditMixin,
    ObjectAttributeValuesByGuidMixin,
    ObjectSnapshotInfoMixin,
    ObjectSnapshotReadonlyObjectsMixin,
    ObjectVisibilitiesMixin,
    ObjectCheckVisibilityAvailableMixin,
    ObjectLoadDescriptionsMixin,
    ObjectCheckOutVersionsMixin,
    ObjectRollbackCheckOutMixin,
    ObjectCheckAccessRightsForVisibilityMixin,
    ObjectUpdateVisibilitySettingsMixin,
    ObjectPrintMixin,
    ObjectSaveToDiskMixin,
    ObjectSaveToArcCopyMixin,
    ObjectsSelectRequestMixin,
    ObjectsSelectByIdMixin,
    ObjectCheckEditMixin,
    ObjectSetModifyContentDateMixin,
):
    """Объединяет методы раздела объектов (чтение объектов и их атрибутов).

    References:
        Эндпоинты ``/core/api/objects/*`` IPS Server Web API.
    """


__all__ = ["ObjectsAPI"]
