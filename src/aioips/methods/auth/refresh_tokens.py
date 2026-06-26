"""Метод обновления пары токенов сессии IPS."""

from typing import Any

from ...core import APIManager


class RefreshTokensMixin(APIManager):
    """Реализует ``POST /core/api/Auth/refreshTokens`` (``Auth_RefreshTokens``)."""

    async def refresh_tokens(
        self: "RefreshTokensMixin",
        request: dict[str, Any],
    ) -> dict[str, Any]:
        """Обновляет пару токенов сессии IPS, обменивая текущую пару на новую.

        Обменивает имеющуюся пару ``ApiTokensDTO`` (access + refresh) на свежую пару,
        продлевая сессию без повторного ввода логина/пароля. Это явный,
        низкоуровневый вызов: он НЕ трогает внутреннее состояние клиента и НЕ кэширует
        результат. Для повседневной работы клиент сам обновляет токен через
        ``AuthManager`` по истечении срока; этот метод нужен для ручного контроля.

        Когда применять: вручную продлить сессию, имея на руках текущую пару токенов
        (например, полученную ранее через :meth:`authenticate`). Предусловие: текущий
        ``refreshToken`` ещё действителен — иначе сервер вернёт ошибку и потребуется
        повторная :meth:`authenticate`.

        Args:
            request: Тело ``ApiTokensDTO`` как ``dict``. Ключи (camelCase):
                ``accessToken`` (str), ``refreshToken`` (str), ``expireTime``
                (ISO-8601 UTC, str). Передаётся как есть.

        Returns:
            Новый ``ApiTokensDTO`` как ``dict[str, Any]``: ``accessToken``,
            ``refreshToken``, ``expireTime``. Возвращается как есть; пустой ``dict``,
            если сервер вернул не объект.

        Raises:
            IPSAuthError: Если refresh-токен истёк/недействителен (``401``).
            IPSError: При иной ошибке сервера.

        Example:
            async with IPSClient(config=config) as ips:
                fresh = await ips.refresh_tokens(
                    {
                        "accessToken": old_access,
                        "refreshToken": old_refresh,
                        "expireTime": "2026-06-25T10:00:00Z",
                    }
                )
                access = fresh["accessToken"]

        Notes:
            operationId ``Auth_RefreshTokens``; путь
            ``POST /core/api/Auth/refreshTokens``; тело ``ApiTokensDTO``; ответ
            ``ApiTokensDTO``. Имя публичного метода — ``refresh_tokens`` (внутренний
            ``AuthManager`` использует приватный ``_refresh_locked`` — конфликта нет).
            Связанные: :meth:`authenticate`, :meth:`clone_tokens`. Домен: [[auth]].
        """
        data = await self._request("post", "/core/api/Auth/refreshTokens", json=request)
        return data if isinstance(data, dict) else {}
