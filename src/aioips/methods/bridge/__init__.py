"""Методы раздела IPS Bridge (клиентский мост) IPS Web API."""

from .bridge_add_or_update_settings_xml import BridgeAddOrUpdateSettingsXmlMixin
from .bridge_common_settings import BridgeCommonSettingsMixin
from .bridge_create_launch_action import BridgeCreateLaunchActionMixin
from .bridge_create_temp_directory import BridgeCreateTempDirectoryMixin
from .bridge_delete_temp_stored_item import BridgeDeleteTempStoredItemMixin
from .bridge_download_app import BridgeDownloadAppMixin
from .bridge_download_integrated_app_plugin import BridgeDownloadIntegratedAppPluginMixin
from .bridge_download_library import BridgeDownloadLibraryMixin
from .bridge_download_temp_folder_as_zip import BridgeDownloadTempFolderAsZipMixin
from .bridge_extract_zip_file import BridgeExtractZipFileMixin
from .bridge_get_action_list import BridgeGetActionListMixin
from .bridge_get_default_actions import BridgeGetDefaultActionsMixin
from .bridge_get_full_action_list import BridgeGetFullActionListMixin
from .bridge_get_integrators import BridgeGetIntegratorsMixin
from .bridge_get_modifications_history_list import BridgeGetModificationsHistoryListMixin
from .bridge_launch_action_data import BridgeLaunchActionDataMixin
from .bridge_launch_action_info import BridgeLaunchActionInfoMixin
from .bridge_pack_directory_as_zip import BridgePackDirectoryAsZipMixin
from .bridge_plugins import BridgePluginsMixin
from .bridge_remove_integrator import BridgeRemoveIntegratorMixin
from .bridge_remove_launch_action import BridgeRemoveLaunchActionMixin
from .bridge_reset_default_action import BridgeResetDefaultActionMixin
from .bridge_set_default_action import BridgeSetDefaultActionMixin
from .bridge_settings_xml import BridgeSettingsXmlMixin
from .bridge_start_log_history import BridgeStartLogHistoryMixin
from .bridge_stop_log_history import BridgeStopLogHistoryMixin
from .bridge_update_launch_action import BridgeUpdateLaunchActionMixin
from .bridge_upload_file import BridgeUploadFileMixin
from .bridge_upload_large_file_cancel import BridgeUploadLargeFileCancelMixin
from .bridge_upload_large_file_chunk import BridgeUploadLargeFileChunkMixin
from .bridge_upload_large_file_chunk_base64 import BridgeUploadLargeFileChunkBase64Mixin
from .bridge_upload_large_file_request import BridgeUploadLargeFileRequestMixin
from .bridge_user_defined_launch_action import BridgeUserDefinedLaunchActionMixin
from .bridge_user_info import BridgeUserInfoMixin


class BridgeAPI(
    BridgeCommonSettingsMixin,
    BridgeUserInfoMixin,
    BridgePluginsMixin,
    BridgeSettingsXmlMixin,
    BridgeUserDefinedLaunchActionMixin,
    BridgeLaunchActionInfoMixin,
    BridgeLaunchActionDataMixin,
    # read-via-POST (списки действий, интеграторы, история)
    BridgeGetIntegratorsMixin,
    BridgeGetActionListMixin,
    BridgeGetDefaultActionsMixin,
    BridgeGetFullActionListMixin,
    BridgeGetModificationsHistoryListMixin,
    # temp-файлы сессии (мутации, confirm)
    BridgeCreateTempDirectoryMixin,
    BridgeDeleteTempStoredItemMixin,
    BridgeDownloadTempFolderAsZipMixin,
    BridgeExtractZipFileMixin,
    BridgePackDirectoryAsZipMixin,
    BridgeUploadFileMixin,
    BridgeUploadLargeFileRequestMixin,
    BridgeUploadLargeFileChunkMixin,
    BridgeUploadLargeFileChunkBase64Mixin,
    BridgeUploadLargeFileCancelMixin,
    # действия запуска и интеграторы (мутации, confirm)
    BridgeCreateLaunchActionMixin,
    BridgeRemoveLaunchActionMixin,
    BridgeUpdateLaunchActionMixin,
    BridgeSetDefaultActionMixin,
    BridgeResetDefaultActionMixin,
    BridgeAddOrUpdateSettingsXmlMixin,
    BridgeRemoveIntegratorMixin,
    # лог истории модификаций сессии
    BridgeStartLogHistoryMixin,
    BridgeStopLogHistoryMixin,
    BridgeDownloadAppMixin,
    BridgeDownloadIntegratedAppPluginMixin,
    BridgeDownloadLibraryMixin,
):
    """Объединяет методы раздела IPS Bridge (клиентский мост).

    References:
        Эндпоинты ``/core/api/Bridge/*`` IPS Server Web API.
    """


__all__ = ["BridgeAPI"]
