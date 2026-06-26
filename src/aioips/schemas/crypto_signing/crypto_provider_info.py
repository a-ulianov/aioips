"""Схема сведений о криптопровайдере для формирования ЭЦП.

References:
    ``GET /core/api/cryptoSigning/objectEncodedHash`` — тело запроса
    ``CryptoProviderInfoDTO`` (флаги — ``CspProviderFlagsDTO``).
"""

from enum import StrEnum

from pydantic import Field

from ..base import IPSModel


class CspProviderFlags(StrEnum):
    """Флаги криптопровайдера CSP (``CspProviderFlagsDTO``).

    Управляют поведением провайдера при доступе к ключевому контейнеру: где искать
    ключи, можно ли их экспортировать, нужно ли подтверждение пользователя и т. п.

    Attributes:
        NO_FLAGS: Без флагов (поведение по умолчанию).
        USE_MACHINE_KEY_STORE: Использовать хранилище ключей машины, а не пользователя.
        USE_DEFAULT_KEY_CONTAINER: Использовать контейнер ключей по умолчанию.
        USE_NON_EXPORTABLE_KEY: Использовать неэкспортируемый ключ.
        USE_EXISTING_KEY: Использовать существующий ключ (не создавать новый).
        USE_ARCHIVABLE_KEY: Использовать архивируемый ключ.
        USE_USER_PROTECTED_KEY: Использовать ключ с защитой паролем пользователя.
        NO_PROMPT: Не выводить диалоги/запросы пользователю.
        CREATE_EPHEMERAL_KEY: Создать временный (эфемерный) ключ.
    """

    NO_FLAGS = "noFlags"
    USE_MACHINE_KEY_STORE = "useMachineKeyStore"
    USE_DEFAULT_KEY_CONTAINER = "useDefaultKeyContainer"
    USE_NON_EXPORTABLE_KEY = "useNonExportableKey"
    USE_EXISTING_KEY = "useExistingKey"
    USE_ARCHIVABLE_KEY = "useArchivableKey"
    USE_USER_PROTECTED_KEY = "useUserProtectedKey"
    NO_PROMPT = "noPrompt"
    CREATE_EPHEMERAL_KEY = "createEphemeralKey"


class CryptoProviderInfo(IPSModel):
    """Сведения о криптопровайдере для подписания объекта (``CryptoProviderInfoDTO``).

    Передаётся телом запроса в :meth:`object_encoded_hash`: описывает, какой
    криптопровайдер и ключевой контейнер использовать для вычисления хэша,
    подписываемого ЭЦП. Все поля необязательны — конкретный набор зависит от
    конфигурации рабочего места и выбранного провайдера.

    Attributes:
        provider_type: Числовой тип криптопровайдера (код CSP).
        provider_name: Имя криптопровайдера. ``None`` — провайдер по умолчанию.
        container_name: Имя ключевого контейнера. ``None`` — контейнер по умолчанию.
        key_number: Номер ключа: задаёт назначение асимметричного ключа (подпись или
            обмен).
        flags: Флаг поведения провайдера (см. :class:`CspProviderFlags`).
    """

    provider_type: int = Field(default=0, description="Числовой тип криптопровайдера (CSP)")
    provider_name: str | None = Field(default=None, description="Имя криптопровайдера")
    container_name: str | None = Field(default=None, description="Имя ключевого контейнера")
    key_number: int = Field(default=0, description="Номер ключа (подпись или обмен)")
    flags: CspProviderFlags | None = Field(default=None, description="Флаг поведения провайдера")
