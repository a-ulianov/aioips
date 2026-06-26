"""Метод получения настроек ЭЦП."""

from ...core import APIManager
from ...schemas.crypto_signing import SigningSettings


class SigningSettingsMixin(APIManager):
    """Реализует ``GET /core/api/cryptoSigning/signingSettings``.

    operationId ``CryptoSigning_GetSigningSettings``.
    """

    async def signing_settings(self: "SigningSettingsMixin") -> SigningSettings:
        """Возвращает глобальные настройки подсистемы ЭЦП IPS.

        Применяют, чтобы узнать действующую конфигурацию подписания до начала работы с
        ЭЦП: нужно ли проверять сертификаты через сервер отзыва, в каком режиме
        (online/offline) и включён ли режим разработчика. Эти параметры влияют на
        поведение подписания/проверки, инициируемого через :meth:`object_encoded_hash`,
        и на интерпретацию сведений из :meth:`sign_info_stream`. Предусловий нет.

        Returns:
            Настройки ЭЦП по схеме :class:`SigningSettings`: ``do_revocation`` (проверять
            сертификаты), ``revocation_mode`` (режим проверки), ``signs_developer_mode``
            (режим разработчика).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                settings = await ips.signing_settings()
                if settings.do_revocation:
                    print("Проверка сертификатов включена, режим:", settings.revocation_mode)

        Notes:
            operationId ``CryptoSigning_GetSigningSettings``; путь
            ``GET /core/api/cryptoSigning/signingSettings`` (``SigningSettingsDTO``).
        """
        data = await self._request("get", "/core/api/cryptoSigning/signingSettings")
        return SigningSettings.model_validate(data)
