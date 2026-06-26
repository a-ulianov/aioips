"""Метод получения опций входа (роли и уровни доступа) по имени пользователя."""

from ...core import APIManager
from ...schemas.auth import AuthOptions


class LoginOptionsMixin(APIManager):
    """Mixin метода «опции входа» IPS Web API.

    Подмешивает в :class:`IPSClient` метод :meth:`login_options` —
    обёртку над ``GET /core/api/Auth/logins/{loginName}/options``: получает
    доступные пользователю роли и уровни доступа без аутентификации (без пароля).

    References:
        Раздел ``/core/api/Auth/*``. Домен: [[auth]].
    """

    async def login_options(self: "LoginOptionsMixin", login_name: str) -> AuthOptions:
        """Возвращает роли и уровни доступа, доступные пользователю при входе.

        Назначение: узнать состав ролей и уровней доступа конкретного логина
        **до аутентификации** — пароль не требуется и не передаётся. Это первый
        (необязательный) шаг двухшаговой схемы входа IPS: сначала опции, затем
        ``authenticate`` с выбранными ``roleID``/``accessLevelID``.

        Когда применять:
            - перед вызовом аутентификации показать пользователю, под какой ролью
              и уровнем доступа он может войти;
            - резолвить человекочитаемое имя роли (``role_name``) в числовой
              ``roleID``, который требует тело ``authenticate``;
            - проверить, существует ли логин и какие у него полномочия, без знания
              пароля.

        Предусловия: авторизация не нужна (эндпоинт публичный); требуется лишь
        сетевой доступ к серверу IPS.

        Args:
            login_name: Имя для входа (логин) пользователя IPS, напр. ``"your-login"``.
                Подставляется в путь URL (URL-экранируется автоматически).

        Returns:
            :class:`AuthOptions` — два списка:

            - ``roles`` (:class:`AuthRole`) — доступные роли, у каждой ``id``
              (числовой ``roleID`` для ``authenticate``) и ``name`` (имя роли);
            - ``access_levels`` (:class:`AuthAccessLevel`) — доступные уровни
              доступа, у каждого ``id`` (``accessLevelID``) и ``name``.

            Списки могут быть пустыми (логин без назначенных ролей/уровней).
            ``None`` не возвращается.

        Raises:
            IPSError: При ошибочном ответе сервера (например, неизвестный логин —
                см. маппинг кодов в ``core/exceptions.py``).

        Example:
            >>> async with IPSClient(config=config) as ips:
            ...     options = await ips.login_options("your-login")
            ...     role_ids = {role.name: role.id for role in options.roles}
            ...     # role_ids -> {"Администратор": 10, ...}; берём id для authenticate

        Notes:
            operationId: ``GET /core/api/Auth/logins/{loginName}/options``
            (``AuthOptionsDTO``). Связанные методы: аутентификация
            (``AuthManager.authenticate`` использует возвращённый ``roleID``),
            :meth:`user_info` (какая роль/уровень фактически активны после
            входа). Домен: [[auth]], [[ips-object-model]].
        """
        data = await self._auth.login_options(login_name)
        return AuthOptions.model_validate(data)
