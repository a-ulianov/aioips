"""Методы раздела Single Sign-On (SSO) IPS Web API."""

from .kerberos_auth_options import KerberosAuthOptionsMixin
from .krb5_authenticate import Krb5AuthenticateMixin


class SsoAPI(KerberosAuthOptionsMixin, Krb5AuthenticateMixin):
    """Объединяет методы раздела Single Sign-On (SSO).

    References:
        Эндпоинты ``/core/api/sso/*`` IPS Server Web API.
    """


__all__ = ["SsoAPI"]
