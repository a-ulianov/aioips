"""Методы раздела справочной системы IMBASE IPS Web API."""

from .imbase_add_from_im_base import ImBaseAddFromImBaseMixin
from .imbase_add_to_favorite_folder import ImBaseAddToFavoriteFolderMixin
from .imbase_attribute_existing_values import ImBaseAttributeExistingValuesMixin
from .imbase_attribute_existing_values_with_progress import (
    ImBaseAttributeExistingValuesWithProgressMixin,
)
from .imbase_catalog_id_by_object import ImBaseCatalogIdByObjectMixin
from .imbase_catalogs import ImBaseCatalogsMixin
from .imbase_client_cache_state import ImBaseClientCacheStateMixin
from .imbase_common_params import ImBaseCommonParamsMixin
from .imbase_create_object import ImBaseCreateObjectMixin
from .imbase_display_mode_options import ImBaseDisplayModeOptionsMixin
from .imbase_extended_item import ImBaseExtendedItemMixin
from .imbase_favorite_folders_count import ImBaseFavoriteFoldersCountMixin
from .imbase_fill_object_attributes import ImBaseFillObjectAttributesMixin
from .imbase_find_by_index import ImBaseFindByIndexMixin
from .imbase_find_in_tables import ImBaseFindInTablesMixin
from .imbase_find_in_tables_with_progress import ImBaseFindInTablesWithProgressMixin
from .imbase_indexes import ImBaseIndexesMixin
from .imbase_linked_object_path import ImBaseLinkedObjectPathMixin
from .imbase_object_applicability import ImBaseObjectApplicabilityMixin
from .imbase_object_by_id_references_names import ImBaseObjectByIdReferencesNamesMixin
from .imbase_object_create_info import ImBaseObjectCreateInfoMixin
from .imbase_object_linked_table_record_attributes import (
    ImBaseObjectLinkedTableRecordAttributesMixin,
)
from .imbase_object_path import ImBaseObjectPathMixin
from .imbase_object_path_by_key import ImBaseObjectPathByKeyMixin
from .imbase_object_references_names import ImBaseObjectReferencesNamesMixin
from .imbase_record_references_names import ImBaseRecordReferencesNamesMixin
from .imbase_remove_from_favorites import ImBaseRemoveFromFavoritesMixin
from .imbase_restrictive_applicability_cache import ImBaseRestrictiveApplicabilityCacheMixin
from .imbase_role_display_mode_options import ImBaseRoleDisplayModeOptionsMixin
from .imbase_rtf_to_plain_text import ImBaseRtfToPlainTextMixin
from .imbase_rtf_to_svg import ImBaseRtfToSvgMixin
from .imbase_supported_catalogs import ImBaseSupportedCatalogsMixin
from .imbase_table_check_composition import ImBaseTableCheckCompositionMixin
from .imbase_table_created_objects import ImBaseTableCreatedObjectsMixin
from .imbase_table_data import ImBaseTableDataMixin
from .imbase_table_display_settings import ImBaseTableDisplaySettingsMixin
from .imbase_table_mix_data import ImBaseTableMixDataMixin
from .imbase_table_record_mix_usage import ImBaseTableRecordMixUsageMixin
from .imbase_table_search_links import ImBaseTableSearchLinksMixin
from .imbase_table_user_filter import ImBaseTableUserFilterMixin
from .imbase_terminal_folder_ids import ImBaseTerminalFolderIdsMixin
from .imbase_text_note_by_guid import ImBaseTextNoteByGuidMixin
from .imbase_user_params import ImBaseUserParamsMixin


class ImBaseAPI(
    ImBaseCatalogsMixin,
    ImBaseSupportedCatalogsMixin,
    ImBaseClientCacheStateMixin,
    ImBaseDisplayModeOptionsMixin,
    ImBaseIndexesMixin,
    # object / params
    ImBaseExtendedItemMixin,
    ImBaseObjectPathMixin,
    ImBaseLinkedObjectPathMixin,
    ImBaseObjectPathByKeyMixin,
    ImBaseTextNoteByGuidMixin,
    ImBaseObjectCreateInfoMixin,
    ImBaseCatalogIdByObjectMixin,
    ImBaseFavoriteFoldersCountMixin,
    ImBaseObjectApplicabilityMixin,
    ImBaseRestrictiveApplicabilityCacheMixin,
    ImBaseCommonParamsMixin,
    ImBaseUserParamsMixin,
    ImBaseRoleDisplayModeOptionsMixin,
    ImBaseTerminalFolderIdsMixin,
    # table / links
    ImBaseTableDataMixin,
    ImBaseTableDisplaySettingsMixin,
    ImBaseTableUserFilterMixin,
    ImBaseTableCreatedObjectsMixin,
    ImBaseTableRecordMixUsageMixin,
    ImBaseTableCheckCompositionMixin,
    ImBaseTableSearchLinksMixin,
    ImBaseObjectLinkedTableRecordAttributesMixin,
    ImBaseTableMixDataMixin,
    # converters / resolvers / favorites (safe ops)
    ImBaseRtfToPlainTextMixin,
    ImBaseRtfToSvgMixin,
    ImBaseObjectReferencesNamesMixin,
    ImBaseObjectByIdReferencesNamesMixin,
    ImBaseRecordReferencesNamesMixin,
    ImBaseAddToFavoriteFolderMixin,
    ImBaseRemoveFromFavoritesMixin,
    ImBaseFindInTablesMixin,
    ImBaseFindByIndexMixin,
    ImBaseAttributeExistingValuesMixin,
    # writes (мутации, confirm) + progress-стримы
    ImBaseCreateObjectMixin,
    ImBaseAddFromImBaseMixin,
    ImBaseFillObjectAttributesMixin,
    ImBaseFindInTablesWithProgressMixin,
    ImBaseAttributeExistingValuesWithProgressMixin,
):
    """Объединяет методы раздела справочной системы IMBASE.

    References:
        Эндпоинты ``/core/api/imbase/*`` IPS Server Web API.
    """


__all__ = ["ImBaseAPI"]
