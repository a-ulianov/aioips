"""Pydantic-схемы запросов и ответов IPS Web API."""

from .auth import AuthAccessLevel, AuthOptions, AuthRole
from .base import IPSModel
from .metadata import ObjectType
from .objects import (
    Attribute,
    AttributeResult,
    AttributeValues,
    ObjectDto,
    ObjectSelectResult,
    QuickObjectInfo,
    SelectCondition,
)
from .users import CurrentUserInfo

__all__ = [
    "Attribute",
    "AttributeResult",
    "AttributeValues",
    "AuthAccessLevel",
    "AuthOptions",
    "AuthRole",
    "CurrentUserInfo",
    "IPSModel",
    "ObjectDto",
    "ObjectSelectResult",
    "ObjectType",
    "QuickObjectInfo",
    "SelectCondition",
]
