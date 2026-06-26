"""Схемы раздела снимков состава (snapshots) IPS Web API."""

from .create_snapshot import CreateSnapshot
from .update_snapshot import UpdateSnapshot

__all__ = [
    "CreateSnapshot",
    "UpdateSnapshot",
]
