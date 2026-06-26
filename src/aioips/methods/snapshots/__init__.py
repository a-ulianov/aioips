"""Методы раздела снимков состава (snapshots) IPS Web API."""

from .create_snapshot import CreateSnapshotMixin
from .delete_snapshot import DeleteSnapshotMixin
from .snapshot_composition import SnapshotCompositionMixin
from .update_snapshot import UpdateSnapshotMixin


class SnapshotsAPI(
    SnapshotCompositionMixin,
    CreateSnapshotMixin,
    UpdateSnapshotMixin,
    DeleteSnapshotMixin,
):
    """Объединяет методы раздела снимков состава.

    References:
        Эндпоинты ``/core/api/snapshots/*`` IPS Server Web API.
    """


__all__ = ["SnapshotsAPI"]
