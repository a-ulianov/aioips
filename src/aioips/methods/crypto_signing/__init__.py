"""Методы раздела ЭЦП (криптографической подписи) IPS Web API."""

from .create_crypto_sign import CreateCryptoSignMixin
from .create_separated_crypto_sign import CreateSeparatedCryptoSignMixin
from .object_encoded_hash import ObjectEncodedHashMixin
from .sign_info_stream import SignInfoStreamMixin
from .signing_settings import SigningSettingsMixin


class CryptoSigningAPI(
    ObjectEncodedHashMixin,
    SignInfoStreamMixin,
    SigningSettingsMixin,
    CreateCryptoSignMixin,
    CreateSeparatedCryptoSignMixin,
):
    """Объединяет методы раздела ЭЦП (чтение данных подписи объектов).

    References:
        Эндпоинты ``/core/api/cryptoSigning/*`` IPS Server Web API.
    """


__all__ = ["CryptoSigningAPI"]
