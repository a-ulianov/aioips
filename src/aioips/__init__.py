"""aioips — асинхронный pydantic-клиент для IPS Server Web API.

Библиотека предоставляет асинхронный (async/await) интерфейс к REST API системы
IPS (Intermech Professional Solutions): авторизацию по JWT с автоматическим
обновлением токена, типизированные pydantic-схемы запросов и ответов, повторы
при транзиентных ошибках и понятную иерархию исключений.

References:
    Репозиторий проекта: https://github.com/a-ulianov/aioips

Notes:
    - Async-first дизайн на базе aiohttp.
    - Авторизация по логину/паролю (JWT) либо готовым access-токеном.
    - Автоматическое обновление токена и обработка ответа 401.
    - Все публичные методы снабжены docstrings на русском с примерами.

Examples:
    import asyncio

    from aioips import IPSClient, IPSConfig

    async def get_object_types() -> None:
        config = IPSConfig(
            base_url="http://your-ips-host:8080",
            login_name="your-login",
            password="...",
            role_name="Администратор",
        )
        async with IPSClient(config=config) as ips:
            return await ips.object_types()

    if __name__ == "__main__":
        asyncio.run(get_object_types())
"""

from .client import IPSClient
from .core import (
    IPSAuthError,
    IPSClientError,
    IPSConfig,
    IPSConflictError,
    IPSConnectionError,
    IPSError,
    IPSForbiddenError,
    IPSNotFoundError,
    IPSServerError,
    IPSTooManyRequestsError,
    MetricsHook,
    RequestMetric,
)
from .infrastructure.logging import configure_logging, get_logger

__version__ = "1.0.0"
__author__ = "Alexander Ulianov"
__repository__ = "https://github.com/a-ulianov/aioips"

logger = get_logger()

__all__ = [
    "IPSAuthError",
    "IPSClient",
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
    "configure_logging",
    "get_logger",
    "logger",
]
