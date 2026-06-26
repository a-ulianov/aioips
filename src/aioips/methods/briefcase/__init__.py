"""Методы раздела Портфеля (briefcase) IPS Web API."""

from .briefcase_cancel_export import BriefcaseCancelExportMixin
from .briefcase_cancel_import import BriefcaseCancelImportMixin
from .briefcase_check_metadata_cancel import BriefcaseCheckMetadataCancelMixin
from .briefcase_check_metadata_only_start import BriefcaseCheckMetadataOnlyStartMixin
from .briefcase_check_metadata_result import BriefcaseCheckMetadataResultMixin
from .briefcase_check_metadata_start import BriefcaseCheckMetadataStartMixin
from .briefcase_export_progress import BriefcaseExportProgressMixin
from .briefcase_start_export import BriefcaseStartExportMixin
from .briefcase_start_import import BriefcaseStartImportMixin
from .briefcase_status import BriefcaseStatusMixin


class BriefcaseAPI(
    BriefcaseStatusMixin,
    BriefcaseExportProgressMixin,
    BriefcaseCheckMetadataResultMixin,
    BriefcaseCancelExportMixin,
    BriefcaseCancelImportMixin,
    BriefcaseCheckMetadataCancelMixin,
    BriefcaseCheckMetadataOnlyStartMixin,
    BriefcaseCheckMetadataStartMixin,
    BriefcaseStartExportMixin,
    BriefcaseStartImportMixin,
):
    """Объединяет методы раздела Портфеля (экспорт/импорт объектов).

    Реализовано безопасное подмножество: запросы статуса/прогресса/результата проверки
    (read) и отмена текущих операций (безопасный no-op, если ничего не запущено). Тяжёлые
    мутации (``StartExport``/``StartImport``) намеренно не включены.

    References:
        Эндпоинты ``/core/api/briefcase/*`` IPS Server Web API.
    """


__all__ = ["BriefcaseAPI"]
