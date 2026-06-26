"""Метод аутентификации IPS по Kerberos/SSO (получение токенов сессии)."""

from typing import Any

from ...core import APIManager


class Krb5AuthenticateMixin(APIManager):
    """Реализует ``POST /core/api/sso/krb5/authenticate`` (``Sso_AuthenticateWithKerberos``)."""

    async def sso_krb5_authenticate(
        self: "Krb5AuthenticateMixin",
        request: dict[str, Any],
    ) -> dict[str, Any]:
        """Аутентифицирует пользователя по Kerberos/SSO и возвращает токены сессии.

        Выполняет вход в IPS средствами доменной аутентификации SPNEGO/Kerberos
        (Single Sign-On) — без явной передачи логина и пароля — и при успехе отдаёт
        пару JWT-токенов ``ApiTokensDTO``. Это явный низкоуровневый вызов: внутреннее
        состояние клиента он не изменяет и результат не кэширует.

        Когда применять: войти в IPS под текущей доменной учётной записью без пароля,
        выбрав конкретные роль/уровень доступа. Доступные роли/уровни (и имя входа)
        предварительно можно узнать через :meth:`kerberos_auth_options`.

        Предусловия: запрос должен нести корректный SPNEGO/Kerberos-контекст
        (доменная среда). При неуспешной Kerberos-аутентификации сервер отвечает
        ``401`` (метод поднимет исключение).

        Args:
            request: Тело ``SsoAuthRequestDTO`` как ``dict``. Ключи (camelCase):
                ``roleID`` (числовой id роли, ``int64``), ``accessLevelID`` (id уровня
                доступа, ``int32``). Логин/пароль не передаются — личность определяется
                Kerberos-контекстом. Передаётся как есть.

        Returns:
            ``ApiTokensDTO`` как ``dict[str, Any]``: ``accessToken`` (str),
            ``refreshToken`` (str), ``expireTime`` (ISO-8601 UTC, str). Возвращается
            как есть; пустой ``dict``, если сервер вернул не объект.

        Raises:
            IPSAuthError: При неуспешной Kerberos-аутентификации (``401``) или
                отказе доступа (``403``).
            IPSError: При иной ошибке сервера.

        Example:
            async with IPSClient(config=config) as ips:
                tokens = await ips.sso_krb5_authenticate({"roleID": 10, "accessLevelID": 0})
                access = tokens["accessToken"]

        Notes:
            operationId ``Sso_AuthenticateWithKerberos``; путь
            ``POST /core/api/sso/krb5/authenticate``; тело ``SsoAuthRequestDTO``; ответ
            ``ApiTokensDTO``. Связанные: :meth:`kerberos_auth_options`,
            :meth:`refresh_tokens`. Домен: разделу авторизации.
        """
        data = await self._request("post", "/core/api/sso/krb5/authenticate", json=request)
        return data if isinstance(data, dict) else {}
