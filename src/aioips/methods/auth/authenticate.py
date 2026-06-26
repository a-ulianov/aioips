"""Метод аутентификации пользователя IPS (обмен логина/пароля на токены)."""

from typing import Any

from ...core import APIManager


class AuthenticateMixin(APIManager):
    """Реализует ``POST /core/api/Auth/authenticate`` (``Auth_Authenticate``)."""

    async def authenticate(
        self: "AuthenticateMixin",
        request: dict[str, Any],
    ) -> dict[str, Any]:
        """Аутентифицирует пользователя IPS и возвращает пару токенов сессии.

        Обменивает логин/пароль (и выбранные роль/уровень доступа) на пару JWT-токенов
        ``ApiTokensDTO``. Это явный, низкоуровневый вызов аутентификации: он НЕ изменяет
        внутреннее состояние клиента и НЕ кэширует токены — полученную пару вызывающий
        распоряжается сам. Для повседневной работы клиент сам управляет токеном через
        ``AuthManager`` (по логину/паролю из конфигурации); этот метод нужен, когда
        требуется ручной контроль (получить токены для другого пользователя/роли,
        интеграция, тесты).

        Когда применять: ручное получение токенов под конкретные ``roleID``/
        ``accessLevelID`` (предварительно их можно узнать через :meth:`login_options`).
        Двухшаговая схема входа: сначала :meth:`login_options`, затем ``authenticate``.

        Args:
            request: Тело ``AuthRequestDTO`` как ``dict``. Ключи (camelCase):
                ``loginName`` (имя входа), ``password`` (пароль), ``passwordType``
                (тип пароля, см. ``AuthPasswordType``), ``roleID`` (числовой id роли,
                ``int64``), ``accessLevelID`` (id уровня доступа, ``int32``). Передаётся
                как есть.

        Returns:
            ``ApiTokensDTO`` как ``dict[str, Any]``: ``accessToken`` (str),
            ``refreshToken`` (str), ``expireTime`` (ISO-8601 UTC, str). Возвращается
            как есть; пустой ``dict``, если сервер вернул не объект.

        Raises:
            IPSAuthError: При неверных учётных данных (``401``) или отказе (``403``).
            IPSError: При иной ошибке сервера.

        Example:
            async with IPSClient(config=config) as ips:
                tokens = await ips.authenticate(
                    {
                        "loginName": "your-login",
                        "password": "secret",
                        "passwordType": 0,
                        "roleID": 10,
                        "accessLevelID": 0,
                    }
                )
                access = tokens["accessToken"]

        Notes:
            operationId ``Auth_Authenticate``; путь ``POST /core/api/Auth/authenticate``;
            тело ``AuthRequestDTO``; ответ ``ApiTokensDTO``. Имя публичного метода —
            ``authenticate`` (внутренний жизненный цикл токена ``AuthManager`` использует
            приватный ``_authenticate_locked`` и не конфликтует). Связанные:
            :meth:`login_options`, :meth:`refresh_tokens`, :meth:`clone_tokens`.
            Домен: разделу авторизации.
        """
        data = await self._request("post", "/core/api/Auth/authenticate", json=request)
        return data if isinstance(data, dict) else {}
