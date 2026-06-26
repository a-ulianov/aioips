"""Методы раздела метаданных IPS Web API."""

from .all_attributes_for_object_type_list import AllAttributesForObjectTypeListMixin
from .all_attributes_for_object_type_list_by_guid import (
    AllAttributesForObjectTypeListByGuidMixin,
)
from .all_attributes_for_relation_type_list import AllAttributesForRelationTypeListMixin
from .all_attributes_for_relation_type_list_by_guid import (
    AllAttributesForRelationTypeListByGuidMixin,
)
from .applicabilities import ApplicabilitiesMixin
from .applicability import ApplicabilityMixin
from .applicability_child_object_type_guids import ApplicabilityChildObjectTypeGuidsMixin
from .applicability_child_object_type_guids_by_guids import (
    ApplicabilityChildObjectTypeGuidsByGuidsMixin,
)
from .applicability_child_object_type_guids_by_parent_guid_relation_guids import (
    ApplicabilityChildObjectTypeGuidsByParentGuidRelationGuidsMixin,
)
from .applicability_child_object_type_guids_by_parent_id_relation_ids import (
    ApplicabilityChildObjectTypeGuidsByParentIdRelationIdsMixin,
)
from .applicability_child_object_type_ids import ApplicabilityChildObjectTypeIdsMixin
from .applicability_child_object_type_ids_by_guids import (
    ApplicabilityChildObjectTypeIdsByGuidsMixin,
)
from .applicability_child_object_type_ids_by_parent_guid_relation_guids import (
    ApplicabilityChildObjectTypeIdsByParentGuidRelationGuidsMixin,
)
from .applicability_child_object_types import ApplicabilityChildObjectTypesMixin
from .applicability_child_object_types_by_guids import ApplicabilityChildObjectTypesByGuidsMixin
from .applicability_relation_type_guids import ApplicabilityRelationTypeGuidsMixin
from .applicability_relation_type_guids_by_guid import ApplicabilityRelationTypeGuidsByGuidMixin
from .applicability_relation_type_ids import ApplicabilityRelationTypeIdsMixin
from .applicability_relation_type_ids_by_guid import ApplicabilityRelationTypeIdsByGuidMixin
from .attribute_for_object_type import AttributeForObjectTypeMixin
from .attribute_for_object_type_by_guids import AttributeForObjectTypeByGuidsMixin
from .attribute_for_object_type_list import AttributeForObjectTypeListMixin
from .attribute_for_object_type_list_by_guid import AttributeForObjectTypeListByGuidMixin
from .attribute_for_relation_type import AttributeForRelationTypeMixin
from .attribute_for_relation_type_by_guids import AttributeForRelationTypeByGuidsMixin
from .attribute_for_relation_type_list import AttributeForRelationTypeListMixin
from .attribute_for_relation_type_list_by_guid import AttributeForRelationTypeListByGuidMixin
from .attribute_group import AttributeGroupMixin
from .attribute_group_by_guid import AttributeGroupByGuidMixin
from .attribute_group_guid import AttributeGroupGuidMixin
from .attribute_group_id_by_guid import AttributeGroupIdByGuidMixin
from .attribute_has_possible_values import AttributeHasPossibleValuesMixin
from .attribute_has_possible_values_by_guid import AttributeHasPossibleValuesByGuidMixin
from .attribute_has_system_data import AttributeHasSystemDataMixin
from .attribute_has_system_data_by_guid import AttributeHasSystemDataByGuidMixin
from .attribute_is_gridable import AttributeIsGridableMixin
from .attribute_is_gridable_by_guid import AttributeIsGridableByGuidMixin
from .attribute_is_in_use import AttributeIsInUseMixin
from .attribute_is_in_use_by_guid import AttributeIsInUseByGuidMixin
from .attribute_linked_object_type_ids import AttributeLinkedObjectTypeIdsMixin
from .attribute_supports_object_links import AttributeSupportsObjectLinksMixin
from .attribute_type import AttributeTypeMixin
from .attribute_type_applicability import AttributeTypeApplicabilityMixin
from .attribute_type_applicability_by_guid import AttributeTypeApplicabilityByGuidMixin
from .attribute_type_by_guid import AttributeTypeByGuidMixin
from .attribute_type_exists import AttributeTypeExistsMixin
from .attribute_type_exists_by_guid import AttributeTypeExistsByGuidMixin
from .attribute_type_guid import AttributeTypeGuidMixin
from .attribute_type_guid_by_name import AttributeTypeGuidByNameMixin
from .attribute_type_guids import AttributeTypeGuidsMixin
from .attribute_type_id_by_guid import AttributeTypeIdByGuidMixin
from .attribute_type_id_by_name import AttributeTypeIdByNameMixin
from .attribute_type_ids import AttributeTypeIdsMixin
from .attribute_type_name import AttributeTypeNameMixin
from .attribute_type_name_by_guid import AttributeTypeNameByGuidMixin
from .attribute_types import AttributeTypesMixin
from .attributes_in_group_guids import AttributesInGroupGuidsMixin
from .attributes_in_group_guids_by_guid import AttributesInGroupGuidsByGuidMixin
from .attributes_in_group_ids import AttributesInGroupIdsMixin
from .attributes_in_group_ids_by_guid import AttributesInGroupIdsByGuidMixin
from .can_add_object_type_to_editing_context import CanAddObjectTypeToEditingContextMixin
from .can_add_object_type_to_editing_context_by_guid import (
    CanAddObjectTypeToEditingContextByGuidMixin,
)
from .can_enters_in import CanEntersInMixin
from .child_object_type_ids import ChildObjectTypeIdsMixin
from .children_type_guids import ChildrenTypeGuidsMixin
from .children_type_guids_by_guid import ChildrenTypeGuidsByGuidMixin
from .children_type_guids_recursive import ChildrenTypeGuidsRecursiveMixin
from .children_type_guids_recursive_by_guid import ChildrenTypeGuidsRecursiveByGuidMixin
from .children_type_ids import ChildrenTypeIdsMixin
from .children_type_ids_by_guid import ChildrenTypeIdsByGuidMixin
from .children_type_ids_recursive import ChildrenTypeIdsRecursiveMixin
from .children_type_ids_recursive_by_guid import ChildrenTypeIdsRecursiveByGuidMixin
from .common_parent_object_type_id_by_ids import CommonParentObjectTypeIdByIdsMixin
from .common_parent_object_type_id_by_version_ids import (
    CommonParentObjectTypeIdByVersionIdsMixin,
)
from .common_parent_type_id import CommonParentTypeIdMixin
from .default_relation_type_guid import DefaultRelationTypeGuidMixin
from .default_relation_type_guid_by_guid import DefaultRelationTypeGuidByGuidMixin
from .default_relation_type_id import DefaultRelationTypeIdMixin
from .default_relation_type_id_by_guid import DefaultRelationTypeIdByGuidMixin
from .designed_object_type_guids import DesignedObjectTypeGuidsMixin
from .designed_object_type_ids import DesignedObjectTypeIdsMixin
from .displayable_by_guid import DisplayableByGuidMixin
from .editing_context_object_type_guids import EditingContextObjectTypeGuidsMixin
from .editing_context_object_type_ids import EditingContextObjectTypeIdsMixin
from .editing_context_top_object_type_guids import EditingContextTopObjectTypeGuidsMixin
from .editing_context_top_object_type_ids import EditingContextTopObjectTypeIdsMixin
from .globals_by_guid import GlobalsByGuidMixin
from .groupable_object_type_guids import GroupableObjectTypeGuidsMixin
from .groupable_object_type_ids import GroupableObjectTypeIdsMixin
from .grouping_object_type_guids import GroupingObjectTypeGuidsMixin
from .grouping_object_type_ids import GroupingObjectTypeIdsMixin
from .grouping_relation_type_guids import GroupingRelationTypeGuidsMixin
from .grouping_relation_type_ids import GroupingRelationTypeIdsMixin
from .has_applicability import HasApplicabilityMixin
from .has_applicability_by_guid import HasApplicabilityByGuidMixin
from .has_applicability_full import HasApplicabilityFullMixin
from .has_local_object_type import HasLocalObjectTypeMixin
from .is_editing_context import IsEditingContextMixin
from .is_editing_context_by_guid import IsEditingContextByGuidMixin
from .is_enabled_parent_type import IsEnabledParentTypeMixin
from .is_object_type_child import IsObjectTypeChildMixin
from .is_object_type_child_by_child_id_parent_guid import (
    IsObjectTypeChildByChildIdParentGuidMixin,
)
from .is_object_type_child_by_guids import IsObjectTypeChildByGuidsMixin
from .is_simple_editing_context import IsSimpleEditingContextMixin
from .life_cycle_level import LifeCycleLevelMixin
from .life_cycle_level_by_guid import LifeCycleLevelByGuidMixin
from .life_cycle_level_exists import LifeCycleLevelExistsMixin
from .life_cycle_level_exists_by_guid import LifeCycleLevelExistsByGuidMixin
from .life_cycle_level_guid import LifeCycleLevelGuidMixin
from .life_cycle_level_id_by_guid import LifeCycleLevelIdByGuidMixin
from .life_cycle_level_name import LifeCycleLevelNameMixin
from .life_cycle_level_name_by_guid import LifeCycleLevelNameByGuidMixin
from .life_cycle_levels import LifeCycleLevelsMixin
from .life_cycle_scheme import LifeCycleSchemeMixin
from .life_cycle_scheme_by_guid import LifeCycleSchemeByGuidMixin
from .life_cycle_scheme_exists import LifeCycleSchemeExistsMixin
from .life_cycle_scheme_exists_by_guid import LifeCycleSchemeExistsByGuidMixin
from .life_cycle_scheme_guid import LifeCycleSchemeGuidMixin
from .life_cycle_scheme_id_by_guid import LifeCycleSchemeIdByGuidMixin
from .life_cycle_scheme_name import LifeCycleSchemeNameMixin
from .life_cycle_scheme_name_by_guid import LifeCycleSchemeNameByGuidMixin
from .life_cycle_scheme_steps import LifeCycleSchemeStepsMixin
from .life_cycle_schemes import LifeCycleSchemesMixin
from .life_cycle_step import LifeCycleStepMixin
from .life_cycle_step_by_guid import LifeCycleStepByGuidMixin
from .life_cycle_step_exists import LifeCycleStepExistsMixin
from .life_cycle_step_exists_by_guid import LifeCycleStepExistsByGuidMixin
from .life_cycle_step_guid import LifeCycleStepGuidMixin
from .life_cycle_step_id_by_guid import LifeCycleStepIdByGuidMixin
from .life_cycle_step_name import LifeCycleStepNameMixin
from .life_cycle_step_name_by_guid import LifeCycleStepNameByGuidMixin
from .life_cycle_steps import LifeCycleStepsMixin
from .local_children_type_ids_recursive import LocalChildrenTypeIdsRecursiveMixin
from .local_object_type_children_ids_recursive_by_ids import (
    LocalObjectTypeChildrenIdsRecursiveByIdsMixin,
)
from .metadata_filters import MetadataFiltersMixin
from .metadata_select import MetadataSelectMixin
from .metadata_state import MetadataStateMixin
from .must_append_object_version import MustAppendObjectVersionMixin
from .object_link_attribute_type_ids import ObjectLinkAttributeTypeIdsMixin
from .object_type import ObjectTypeMixin
from .object_type_applicabilities import ObjectTypeApplicabilitiesMixin
from .object_type_applicabilities_by_guid import ObjectTypeApplicabilitiesByGuidMixin
from .object_type_by_guid import ObjectTypeByGuidMixin
from .object_type_children_guids_recursive_by_guids import (
    ObjectTypeChildrenGuidsRecursiveByGuidsMixin,
)
from .object_type_children_ids_recursive_by_ids import (
    ObjectTypeChildrenIdsRecursiveByIdsMixin,
)
from .object_type_exists import ObjectTypeExistsMixin
from .object_type_exists_by_guid import ObjectTypeExistsByGuidMixin
from .object_type_full_name import ObjectTypeFullNameMixin
from .object_type_guid import ObjectTypeGuidMixin
from .object_type_has_design import ObjectTypeHasDesignMixin
from .object_type_has_design_by_guid import ObjectTypeHasDesignByGuidMixin
from .object_type_has_grouping import ObjectTypeHasGroupingMixin
from .object_type_has_grouping_by_guid import ObjectTypeHasGroupingByGuidMixin
from .object_type_has_sorting import ObjectTypeHasSortingMixin
from .object_type_has_sorting_by_guid import ObjectTypeHasSortingByGuidMixin
from .object_type_has_substitution import ObjectTypeHasSubstitutionMixin
from .object_type_has_substitution_by_guid import ObjectTypeHasSubstitutionByGuidMixin
from .object_type_has_visibility_attribute import ObjectTypeHasVisibilityAttributeMixin
from .object_type_has_visibility_attribute_by_guid import (
    ObjectTypeHasVisibilityAttributeByGuidMixin,
)
from .object_type_id_by_guid import ObjectTypeIdByGuidMixin
from .object_type_id_by_name import ObjectTypeIdByNameMixin
from .object_type_is_groupable import ObjectTypeIsGroupableMixin
from .object_type_is_groupable_by_guid import ObjectTypeIsGroupableByGuidMixin
from .object_type_is_local import ObjectTypeIsLocalMixin
from .object_type_is_local_by_guid import ObjectTypeIsLocalByGuidMixin
from .object_type_level import ObjectTypeLevelMixin
from .object_type_life_cycle_steps import ObjectTypeLifeCycleStepsMixin
from .object_type_name import ObjectTypeNameMixin
from .object_type_name_by_guid import ObjectTypeNameByGuidMixin
from .object_type_object_name import ObjectTypeObjectNameMixin
from .object_type_object_name_by_guid import ObjectTypeObjectNameByGuidMixin
from .object_type_parent_applicabilities import ObjectTypeParentApplicabilitiesMixin
from .object_types import ObjectTypesMixin
from .object_types_with_applicabilities_ids import ObjectTypesWithApplicabilitiesIdsMixin
from .object_types_with_enter_in_applicabilities_ids import (
    ObjectTypesWithEnterInApplicabilitiesIdsMixin,
)
from .objects_by_object_type import ObjectsByObjectTypeMixin
from .optimize_child_object_types import OptimizeChildObjectTypesMixin
from .parent_type_guid_by_guid import ParentTypeGuidByGuidMixin
from .parent_type_guids import ParentTypeGuidsMixin
from .parent_type_guids_by_guid import ParentTypeGuidsByGuidMixin
from .parent_type_id import ParentTypeIdMixin
from .parent_type_ids import ParentTypeIdsMixin
from .parent_type_ids_by_guid import ParentTypeIdsByGuidMixin
from .parent_type_ids_reverse import ParentTypeIdsReverseMixin
from .pdm_object_type_is_configurable import PdmObjectTypeIsConfigurableMixin
from .pdm_object_type_is_contextable import PdmObjectTypeIsContextableMixin
from .pdm_object_type_is_root import PdmObjectTypeIsRootMixin
from .pdm_relation_type_is_configurable import PdmRelationTypeIsConfigurableMixin
from .pdm_relation_type_is_partially_configurable import (
    PdmRelationTypeIsPartiallyConfigurableMixin,
)
from .related_formula_attributes_for_object import RelatedFormulaAttributesForObjectMixin
from .related_formula_attributes_for_relation import (
    RelatedFormulaAttributesForRelationMixin,
)
from .relation_type_for_prj_link import RelationTypeForPrjLinkMixin
from .relation_type_has_grouping import RelationTypeHasGroupingMixin
from .relation_type_has_grouping_by_guid import RelationTypeHasGroupingByGuidMixin
from .relation_type_has_sorting import RelationTypeHasSortingMixin
from .relation_type_has_sorting_by_guid import RelationTypeHasSortingByGuidMixin
from .relation_type_has_substitutes import RelationTypeHasSubstitutesMixin
from .relation_type_has_substitutes_by_guid import RelationTypeHasSubstitutesByGuidMixin
from .relation_type_meta import RelationTypeMetaMixin
from .relation_type_meta_by_guid import RelationTypeMetaByGuidMixin
from .relation_type_meta_exists import RelationTypeMetaExistsMixin
from .relation_type_meta_exists_by_guid import RelationTypeMetaExistsByGuidMixin
from .relation_type_meta_guid import RelationTypeMetaGuidMixin
from .relation_type_meta_id_by_guid import RelationTypeMetaIdByGuidMixin
from .relation_type_meta_name import RelationTypeMetaNameMixin
from .relation_type_meta_name_by_guid import RelationTypeMetaNameByGuidMixin
from .relation_types_meta import RelationTypesMetaMixin
from .sorting_object_type_guids import SortingObjectTypeGuidsMixin
from .sorting_object_type_ids import SortingObjectTypeIdsMixin
from .sorting_relation_type_guids import SortingRelationTypeGuidsMixin
from .sorting_relation_type_ids import SortingRelationTypeIdsMixin
from .substitute_object_type_guids import SubstituteObjectTypeGuidsMixin
from .substitute_object_type_ids import SubstituteObjectTypeIdsMixin
from .substitute_relation_type_guids import SubstituteRelationTypeGuidsMixin
from .substitute_relation_type_ids import SubstituteRelationTypeIdsMixin
from .top_object_type_guids import TopObjectTypeGuidsMixin
from .top_object_type_ids import TopObjectTypeIdsMixin
from .top_parent_enabled_object_type_guids_by_guids import (
    TopParentEnabledObjectTypeGuidsByGuidsMixin,
)
from .top_parent_enabled_object_type_ids_by_ids import (
    TopParentEnabledObjectTypeIdsByIdsMixin,
)
from .top_parent_type_id import TopParentTypeIdMixin
from .used_sorted_attribute_ids import UsedSortedAttributeIdsMixin
from .used_sorted_attributes import UsedSortedAttributesMixin
from .used_unsorted_attribute_ids import UsedUnsortedAttributeIdsMixin
from .visibility_object_type_guids import VisibilityObjectTypeGuidsMixin
from .visibility_object_type_ids import VisibilityObjectTypeIdsMixin


class MetadataAPI(
    # objectTypes — основное
    ObjectTypesMixin,
    ObjectTypeMixin,
    ObjectTypeByGuidMixin,
    ObjectTypeIdByNameMixin,
    ObjectsByObjectTypeMixin,
    ObjectTypeLifeCycleStepsMixin,
    # objectTypes — аксессоры
    ObjectTypeExistsMixin,
    ObjectTypeExistsByGuidMixin,
    ObjectTypeIdByGuidMixin,
    ObjectTypeNameMixin,
    ObjectTypeNameByGuidMixin,
    ObjectTypeGuidMixin,
    ObjectTypeFullNameMixin,
    ObjectTypeObjectNameMixin,
    ObjectTypeObjectNameByGuidMixin,
    ObjectTypeIsLocalMixin,
    ObjectTypeIsLocalByGuidMixin,
    # attributeTypes — основное
    AttributeTypesMixin,
    AttributeTypeMixin,
    AttributeTypeByGuidMixin,
    AttributeTypeIdByNameMixin,
    AttributeForObjectTypeListMixin,
    # attributeTypes — аксессоры
    AttributeTypeExistsMixin,
    AttributeTypeExistsByGuidMixin,
    AttributeTypeIdByGuidMixin,
    AttributeTypeNameByGuidMixin,
    AttributeTypeNameMixin,
    AttributeTypeGuidMixin,
    AttributeTypeGuidByNameMixin,
    AttributeTypeIdsMixin,
    AttributeTypeGuidsMixin,
    AttributeHasPossibleValuesMixin,
    AttributeHasPossibleValuesByGuidMixin,
    AttributeHasSystemDataMixin,
    AttributeHasSystemDataByGuidMixin,
    AttributeIsGridableMixin,
    AttributeIsGridableByGuidMixin,
    AttributeSupportsObjectLinksMixin,
    # relationTypes — метаданные
    RelationTypesMetaMixin,
    RelationTypeMetaMixin,
    RelationTypeMetaByGuidMixin,
    RelationTypeMetaExistsMixin,
    RelationTypeMetaExistsByGuidMixin,
    RelationTypeMetaIdByGuidMixin,
    RelationTypeMetaNameMixin,
    RelationTypeMetaNameByGuidMixin,
    RelationTypeMetaGuidMixin,
    DefaultRelationTypeIdMixin,
    DefaultRelationTypeGuidMixin,
    DefaultRelationTypeIdByGuidMixin,
    DefaultRelationTypeGuidByGuidMixin,
    # applicabilities
    ObjectTypeApplicabilitiesMixin,
    ObjectTypeParentApplicabilitiesMixin,
    ChildObjectTypeIdsMixin,
    HasApplicabilityMixin,
    ApplicabilitiesMixin,
    ApplicabilityMixin,
    ObjectTypeApplicabilitiesByGuidMixin,
    HasApplicabilityFullMixin,
    HasApplicabilityByGuidMixin,
    CanEntersInMixin,
    ApplicabilityChildObjectTypesMixin,
    ApplicabilityChildObjectTypeIdsMixin,
    ApplicabilityChildObjectTypeGuidsMixin,
    ApplicabilityChildObjectTypesByGuidsMixin,
    ApplicabilityRelationTypeIdsMixin,
    ApplicabilityRelationTypeGuidsMixin,
    ObjectTypesWithApplicabilitiesIdsMixin,
    ObjectTypesWithEnterInApplicabilitiesIdsMixin,
    # lifeCycleSchemes
    LifeCycleSchemesMixin,
    LifeCycleSchemeMixin,
    LifeCycleSchemeByGuidMixin,
    LifeCycleSchemeStepsMixin,
    LifeCycleSchemeExistsMixin,
    LifeCycleSchemeExistsByGuidMixin,
    LifeCycleSchemeIdByGuidMixin,
    LifeCycleSchemeNameMixin,
    LifeCycleSchemeNameByGuidMixin,
    LifeCycleSchemeGuidMixin,
    # lifeCycleLevels
    LifeCycleLevelsMixin,
    LifeCycleLevelMixin,
    LifeCycleLevelByGuidMixin,
    LifeCycleLevelExistsMixin,
    LifeCycleLevelExistsByGuidMixin,
    LifeCycleLevelIdByGuidMixin,
    LifeCycleLevelNameMixin,
    LifeCycleLevelNameByGuidMixin,
    LifeCycleLevelGuidMixin,
    # lifeCycleSteps — глобальные аксессоры
    LifeCycleStepsMixin,
    LifeCycleStepMixin,
    LifeCycleStepByGuidMixin,
    LifeCycleStepExistsMixin,
    LifeCycleStepExistsByGuidMixin,
    LifeCycleStepIdByGuidMixin,
    LifeCycleStepNameMixin,
    LifeCycleStepNameByGuidMixin,
    LifeCycleStepGuidMixin,
    # grouping
    GroupableObjectTypeIdsMixin,
    GroupableObjectTypeGuidsMixin,
    ObjectTypeIsGroupableMixin,
    ObjectTypeIsGroupableByGuidMixin,
    GroupingObjectTypeIdsMixin,
    GroupingObjectTypeGuidsMixin,
    ObjectTypeHasGroupingMixin,
    ObjectTypeHasGroupingByGuidMixin,
    GroupingRelationTypeIdsMixin,
    GroupingRelationTypeGuidsMixin,
    RelationTypeHasGroupingMixin,
    RelationTypeHasGroupingByGuidMixin,
    # sorting
    SortingObjectTypeIdsMixin,
    SortingObjectTypeGuidsMixin,
    ObjectTypeHasSortingMixin,
    ObjectTypeHasSortingByGuidMixin,
    SortingRelationTypeIdsMixin,
    SortingRelationTypeGuidsMixin,
    RelationTypeHasSortingMixin,
    RelationTypeHasSortingByGuidMixin,
    # editingContext
    EditingContextObjectTypeIdsMixin,
    EditingContextObjectTypeGuidsMixin,
    EditingContextTopObjectTypeIdsMixin,
    EditingContextTopObjectTypeGuidsMixin,
    IsEditingContextMixin,
    IsEditingContextByGuidMixin,
    CanAddObjectTypeToEditingContextMixin,
    CanAddObjectTypeToEditingContextByGuidMixin,
    IsSimpleEditingContextMixin,
    MustAppendObjectVersionMixin,
    # substitution
    SubstituteObjectTypeIdsMixin,
    SubstituteObjectTypeGuidsMixin,
    ObjectTypeHasSubstitutionMixin,
    ObjectTypeHasSubstitutionByGuidMixin,
    SubstituteRelationTypeIdsMixin,
    SubstituteRelationTypeGuidsMixin,
    RelationTypeHasSubstitutesMixin,
    RelationTypeHasSubstitutesByGuidMixin,
    # design
    DesignedObjectTypeIdsMixin,
    DesignedObjectTypeGuidsMixin,
    ObjectTypeHasDesignMixin,
    ObjectTypeHasDesignByGuidMixin,
    # visibility
    VisibilityObjectTypeIdsMixin,
    VisibilityObjectTypeGuidsMixin,
    ObjectTypeHasVisibilityAttributeMixin,
    ObjectTypeHasVisibilityAttributeByGuidMixin,
    # pdm
    PdmObjectTypeIsConfigurableMixin,
    PdmObjectTypeIsContextableMixin,
    PdmObjectTypeIsRootMixin,
    PdmRelationTypeIsConfigurableMixin,
    PdmRelationTypeIsPartiallyConfigurableMixin,
    # attribute-for-type
    AttributeForObjectTypeMixin,
    AttributeForObjectTypeByGuidsMixin,
    AttributeForObjectTypeListByGuidMixin,
    AllAttributesForObjectTypeListMixin,
    AllAttributesForObjectTypeListByGuidMixin,
    AttributeForRelationTypeMixin,
    AttributeForRelationTypeByGuidsMixin,
    AttributeForRelationTypeListMixin,
    AttributeForRelationTypeListByGuidMixin,
    AllAttributesForRelationTypeListMixin,
    AllAttributesForRelationTypeListByGuidMixin,
    UsedSortedAttributesMixin,
    UsedSortedAttributeIdsMixin,
    UsedUnsortedAttributeIdsMixin,
    # attributeGroups
    AttributeGroupMixin,
    AttributeGroupByGuidMixin,
    AttributeGroupIdByGuidMixin,
    AttributeGroupGuidMixin,
    AttributesInGroupIdsMixin,
    AttributesInGroupGuidsMixin,
    AttributesInGroupIdsByGuidMixin,
    AttributesInGroupGuidsByGuidMixin,
    # attributeTypeApplicability
    AttributeTypeApplicabilityMixin,
    AttributeTypeApplicabilityByGuidMixin,
    AttributeIsInUseMixin,
    AttributeIsInUseByGuidMixin,
    # справки атрибутов-ссылок и формул
    AttributeLinkedObjectTypeIdsMixin,
    ObjectLinkAttributeTypeIdsMixin,
    RelationTypeForPrjLinkMixin,
    RelatedFormulaAttributesForObjectMixin,
    RelatedFormulaAttributesForRelationMixin,
    # objectTypeTree — иерархия типов
    ChildrenTypeIdsMixin,
    ChildrenTypeGuidsMixin,
    ChildrenTypeIdsByGuidMixin,
    ChildrenTypeGuidsByGuidMixin,
    ChildrenTypeIdsRecursiveMixin,
    ChildrenTypeGuidsRecursiveMixin,
    ChildrenTypeIdsRecursiveByGuidMixin,
    ChildrenTypeGuidsRecursiveByGuidMixin,
    LocalChildrenTypeIdsRecursiveMixin,
    ParentTypeIdMixin,
    ParentTypeGuidByGuidMixin,
    ParentTypeIdsMixin,
    ParentTypeGuidsMixin,
    ParentTypeIdsByGuidMixin,
    ParentTypeGuidsByGuidMixin,
    ParentTypeIdsReverseMixin,
    TopParentTypeIdMixin,
    CommonParentTypeIdMixin,
    IsObjectTypeChildMixin,
    IsObjectTypeChildByChildIdParentGuidMixin,
    IsObjectTypeChildByGuidsMixin,
    ObjectTypeLevelMixin,
    TopObjectTypeIdsMixin,
    TopObjectTypeGuidsMixin,
    ApplicabilityRelationTypeIdsByGuidMixin,
    ApplicabilityRelationTypeGuidsByGuidMixin,
    ApplicabilityChildObjectTypeIdsByGuidsMixin,
    ApplicabilityChildObjectTypeGuidsByGuidsMixin,
    DisplayableByGuidMixin,
    GlobalsByGuidMixin,
    # POST-чтения метамодели (пакетные применяемость/дерево типов/select/state)
    ApplicabilityChildObjectTypeGuidsByParentGuidRelationGuidsMixin,
    ApplicabilityChildObjectTypeIdsByParentGuidRelationGuidsMixin,
    ApplicabilityChildObjectTypeGuidsByParentIdRelationIdsMixin,
    IsEnabledParentTypeMixin,
    MetadataFiltersMixin,
    ObjectTypeChildrenGuidsRecursiveByGuidsMixin,
    LocalObjectTypeChildrenIdsRecursiveByIdsMixin,
    ObjectTypeChildrenIdsRecursiveByIdsMixin,
    CommonParentObjectTypeIdByIdsMixin,
    CommonParentObjectTypeIdByVersionIdsMixin,
    OptimizeChildObjectTypesMixin,
    TopParentEnabledObjectTypeGuidsByGuidsMixin,
    TopParentEnabledObjectTypeIdsByIdsMixin,
    HasLocalObjectTypeMixin,
    MetadataSelectMixin,
    MetadataStateMixin,
):
    """Объединяет методы раздела метаданных.

    References:
        Эндпоинты ``/core/api/metadata/*`` IPS Server Web API.
    """


__all__ = ["MetadataAPI"]
