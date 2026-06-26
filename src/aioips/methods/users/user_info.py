"""Метод получения информации о текущем пользователе сессии."""

from ...core import APIManager
from ...schemas.users import CurrentUserInfo


class UserInfoMixin(APIManager):
    """Mixin метода «информация о текущем пользователе» IPS Web API.

    Подмешивает в :class:`IPSClient` метод :meth:`user_info` —
    обёртку над ``GET /core/api/currentUsers/userInfo``: кто сейчас в сессии,
    под какой ролью/уровнем доступа и админ ли он.

    References:
        Раздел ``/core/api/currentUsers/*``. Домен: разделу авторизации.
    """

    async def user_info(self: "UserInfoMixin") -> CurrentUserInfo:
        """Возвращает сведения о пользователе текущей авторизованной сессии.

        Назначение: «кто я» для уже выполненного входа — идентификатор сессии,
        активная роль и уровень доступа, признак администратора, имя для входа
        и отображаемое имя.

        Когда применять:
            - проверить, действительна ли сессия (валидный токен → корректный ответ);
            - узнать, под какой ролью/уровнем доступа фактически выполнен вход
              (в отличие от :meth:`login_options`, показывающего лишь доступные
              варианты ДО входа);
            - определить административные права (``is_admin``) для гейтинга
              операций в UI/MCP-инструментах.

        Предусловия: требуется активная авторизованная сессия — клиент должен
        иметь действующий access-токен (получается автоматически при первом
        запросе из логина/пароля конфигурации).

        Returns:
            :class:`CurrentUserInfo`. Значимые поля:

            - ``session_id`` (UUID) — идентификатор текущей сессии;
            - ``login_name`` — имя для входа (логин), может быть ``None``;
            - ``user_name`` — отображаемое имя, может быть ``None``;
            - ``role_version_id`` — версия роли, под которой выполнен вход;
            - ``access_level`` — идентификатор уровня доступа сессии;
            - ``is_admin`` — есть ли административные права;
            - ``user_version_id`` — версия объекта пользователя.

            ``None`` метод не возвращает: при отсутствии/недействительности
            сессии будет исключение, а не пустой результат.

        Raises:
            IPSError: При ошибочном ответе сервера (например, ``401`` —
                сессия недействительна; см. маппинг в ``core/exceptions.py``).

        Example:
            >>> async with IPSClient(config=config) as ips:
            ...     me = await ips.user_info()
            ...     print(me.login_name, me.is_admin)  # 'your-login' True

        Notes:
            operationId: ``GET /core/api/currentUsers/userInfo``
            (``CurrentUserInfoDto``). Связанные методы: :meth:`login_options`
            (роли/уровни ДО входа). ``*_version_id`` — это id ВЕРСИЙ объектов
            (см. различие версия/объект в объектной модели IPS), не id объектов.
            Домен: разделу авторизации.
        """
        data = await self._request("get", "/core/api/currentUsers/userInfo")
        return CurrentUserInfo.model_validate(data)
