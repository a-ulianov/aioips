"""Схемы раздела графических подписей (штампов ЭЦП) IPS Web API."""

from .assigned_sign_graph_group import AssignedSignGraph, AssignedSignGraphGroup
from .rank_graph_signs import RankGraphSigns, RankGraphSignsSettings

__all__ = [
    "AssignedSignGraph",
    "AssignedSignGraphGroup",
    "RankGraphSigns",
    "RankGraphSignsSettings",
]
