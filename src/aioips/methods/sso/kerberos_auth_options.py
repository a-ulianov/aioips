"""Метод получения опций Kerberos-аутентификации текущего пользователя."""

from ...core import APIManager
from ...schemas.sso import SsoAuthOptions


class KerberosAuthOptionsMixin(APIManager):
    """Реализует ``GET /core/api/sso/krb5/currentUser/options``.

    operationId ``Sso_GetKerberosAuthenticationOptions``.
    """

    async def kerberos_auth_options(self: "KerberosAuthOptionsMixin") -> SsoAuthOptions:
        """Возвращает опции аутентификации текущего пользователя по SPNEGO/Kerberos.

        Выполняет аутентификацию по схеме SPNEGO/Kerberos для текущего пользователя
        операционной системы и, при успехе, отдаёт его имя входа в IPS вместе с
        доступными ролями и уровнями доступа. Применяется в сценариях Single Sign-On,
        когда вход выполняется средствами доменной аутентификации без явного ввода
        логина и пароля.

        Когда применять: чтобы определить учётную запись IPS и доступные роли текущего
        доменного пользователя перед входом по SSO. Метод только читает.

        Предусловия: запрос должен нести корректный SPNEGO/Kerberos-контекст. При
        неуспешной или невозможной Kerberos-аутентификации сервер отвечает ``401`` с
        problem details (метод поднимет исключение).

        Returns:
            Опции аутентификации по схеме :class:`SsoAuthOptions`: ``login_name`` — имя
            входа пользователя IPS, ``login_options`` — роли и уровни доступа.

        Raises:
            IPSError: При ошибочном ответе сервера, в частности ``401`` при неуспешной
                Kerberos-аутентификации.

        Example:
            async with IPSClient(config=config) as ips:
                options = await ips.kerberos_auth_options()
                print(options.login_name, len(options.login_options.roles))

        Notes:
            operationId ``Sso_GetKerberosAuthenticationOptions``; путь
            ``GET /core/api/sso/krb5/currentUser/options`` (``SsoAuthOptionsDTO``).
        """
        data = await self._request("get", "/core/api/sso/krb5/currentUser/options")
        return SsoAuthOptions.model_validate(data)
