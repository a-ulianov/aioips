"""Методы раздела архивов IPS Web API."""

from .archive_can_apply_settings import ArchiveCanApplySettingsMixin


class ArchivesAPI(
    ArchiveCanApplySettingsMixin,
):
    """Объединяет методы раздела архивов.

    References:
        Эндпоинты ``/core/api/archives/*`` IPS Server Web API.
    """


__all__ = ["ArchivesAPI"]
