"""Методы раздела лицензий IPS Web API."""

from .generate_client_id import GenerateClientIdMixin
from .licenses_encrypt import LicensesEncryptMixin


class LicensesAPI(GenerateClientIdMixin, LicensesEncryptMixin):
    """Объединяет методы раздела лицензий.

    References:
        Эндпоинты ``/core/api/licenses/*`` IPS Server Web API.
    """


__all__ = ["LicensesAPI"]
