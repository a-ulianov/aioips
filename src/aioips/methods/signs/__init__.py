"""Методы раздела электронной подписи (ЭЦП) IPS Web API."""

from .additional_sign_output_params import AdditionalSignOutputParamsMixin
from .additional_user_output_params import AdditionalUserOutputParamsMixin
from .sign_graphs import SignGraphsMixin
from .sign_ranks import SignRanksMixin


class SignsAPI(
    SignGraphsMixin,
    SignRanksMixin,
    AdditionalSignOutputParamsMixin,
    AdditionalUserOutputParamsMixin,
):
    """Объединяет методы раздела электронной подписи (метаданные ЭЦП).

    References:
        Эндпоинты ``/api/signs/*`` IPS Server Web API.
    """


__all__ = ["SignsAPI"]
