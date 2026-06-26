"""Схема настроек ЭЦП (электронной цифровой подписи) IPS.

References:
    ``GET /core/api/cryptoSigning/signingSettings`` — ``SigningSettingsDTO``.
"""

from pydantic import Field

from ..base import IPSModel


class SigningSettings(IPSModel):
    """Глобальные настройки подписания объектов ЭЦП в IPS.

    Описывает поведение подсистемы криптографической подписи: нужно ли проверять
    сертификаты через сервер отзыва, в каком режиме (online/offline) выполняется
    проверка и включён ли режим разработчика для подписей. Возвращается методом
    :meth:`signing_settings`; на вход подписания не подаётся (read-only DTO).

    Все поля необязательны и имеют дефолты: набор настроек может различаться между
    версиями сервера и конфигурациями, поэтому схема устойчива к отсутствию полей.

    Attributes:
        do_revocation: Проверять сертификаты. Если ``True``, при подписании и проверке
            подписи выполняется дополнительная проверка сертификата через сервер отзыва
            (online или offline — задаётся ``revocation_mode``).
        revocation_mode: Режим дополнительной проверки сертификатов (целочисленный код):
            online (через сеть) или offline (по локальным спискам отзыва). Значим только
            при ``do_revocation = True``.
        signs_developer_mode: Признак режима разработчика для подписей.
    """

    do_revocation: bool = Field(
        default=False,
        description="Проверять сертификаты через сервер отзыва при подписании/проверке",
    )
    revocation_mode: int = Field(
        default=0,
        description="Режим проверки сертификатов: online (сеть) или offline (списки отзыва)",
    )
    signs_developer_mode: bool = Field(default=False, description="Режим разработчика для подписей")
