"""Методы раздела конфигурации сервера IPS Web API (чтение параметров)."""

from .config_read_bool import ConfigReadBoolMixin
from .config_read_date_time import ConfigReadDateTimeMixin
from .config_read_double import ConfigReadDoubleMixin
from .config_read_integer import ConfigReadIntegerMixin
from .config_read_string import ConfigReadStringMixin
from .config_read_string_no_cache import ConfigReadStringNoCacheMixin
from .server_os_platform import ServerOsPlatformMixin


class ConfigAPI(
    ConfigReadBoolMixin,
    ConfigReadStringMixin,
    ConfigReadIntegerMixin,
    ConfigReadDoubleMixin,
    ConfigReadDateTimeMixin,
    ConfigReadStringNoCacheMixin,
    ServerOsPlatformMixin,
):
    """Объединяет методы чтения параметров конфигурации сервера.

    References:
        Эндпоинты ``/core/api/Config/*`` IPS Server Web API.
    """


__all__ = ["ConfigAPI"]
