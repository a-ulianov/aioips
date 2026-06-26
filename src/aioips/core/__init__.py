"""Ядро клиента IPS: конфигурация, авторизация, сессии, обработка запросов."""

from .auth import AuthManager
from .config import IPSConfig
from .core import APIManager
from .exceptions import (
    IPSAuthError,
    IPSClientError,
    IPSConflictError,
    IPSConnectionError,
    IPSError,
    IPSForbiddenError,
    IPSNotFoundError,
    IPSServerError,
    IPSTooManyRequestsError,
    exception_from_response,
)
from .observability import MetricsHook, RequestMetric
from .sessions import SessionManager

__all__ = [
    "APIManager",
    "AuthManager",
    "IPSAuthError",
    "IPSClientError",
    "IPSConfig",
    "IPSConflictError",
    "IPSConnectionError",
    "IPSError",
    "IPSForbiddenError",
    "IPSNotFoundError",
    "IPSServerError",
    "IPSTooManyRequestsError",
    "MetricsHook",
    "RequestMetric",
    "SessionManager",
    "exception_from_response",
]
