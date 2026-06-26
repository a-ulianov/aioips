"""Перечисления, относящиеся к авторизации в IPS."""

from enum import StrEnum


class AuthPasswordType(StrEnum):
    """Способ кодирования пароля в запросе аутентификации (``AuthPasswordType``).

    Передаётся в поле ``passwordType`` при ``POST /core/api/Auth/authenticate``
    и сообщает серверу, как интерпретировать поле ``password``. Соответствует
    параметру конфигурации ``IPSConfig.password_type``.

    Семантика членов:
        PLAIN_TEXT: ``plainText`` — пароль передан как открытый текст.
        BASE64_TEXT: ``base64Text`` — пароль закодирован в Base64.
    """

    PLAIN_TEXT = "plainText"
    BASE64_TEXT = "base64Text"
