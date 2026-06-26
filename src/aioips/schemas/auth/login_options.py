"""Схемы ответа на запрос опций входа (роли и уровни доступа).

Описывают тело ``AuthOptionsDTO`` — список доступных логину ролей и уровней
доступа, возвращаемых до аутентификации (без пароля). Эти ``id`` затем
используются в теле ``authenticate`` как ``roleID``/``accessLevelID``.

References:
    ``GET /core/api/Auth/logins/{loginName}/options`` — ``AuthOptionsDTO``.
    Домен: [[auth]].
"""

from pydantic import Field

from ..base import IPSModel


class AuthRole(IPSModel):
    """Роль, под которой пользователь может войти в IPS.

    Элемент списка ``roles`` ответа «опции входа». Поле ``id`` — это тот самый
    ``roleID``, который передаётся в теле ``authenticate`` для входа под данной
    ролью. JSON-алиасы (camelCase) генерируются автоматически (``id``/``name``).

    Attributes:
        id: Числовой идентификатор роли (``roleID`` для ``authenticate``).
        name: Человекочитаемое имя роли (напр. ``"Администратор"``).
    """

    id: int = Field(description="Идентификатор роли (roleID для authenticate)")
    name: str = Field(description="Имя роли")


class AuthAccessLevel(IPSModel):
    """Уровень доступа, с которым пользователь может войти в IPS.

    Элемент списка ``accessLevels`` ответа «опции входа». Поле ``id`` —
    ``accessLevelID``, передаваемый в теле ``authenticate``. Уровень доступа
    определяет видимость объектов/данных в рамках выбранной роли.

    Attributes:
        id: Числовой идентификатор уровня доступа (``accessLevelID``).
        name: Человекочитаемое имя уровня доступа (напр. ``"Обычный"``).
    """

    id: int = Field(description="Идентификатор уровня доступа (accessLevelID)")
    name: str = Field(description="Имя уровня доступа")


class AuthOptions(IPSModel):
    """Опции входа: роли и уровни доступа, доступные логину (без пароля).

    Ответ ``GET /core/api/Auth/logins/{loginName}/options`` (``AuthOptionsDTO``),
    результат метода :meth:`~aioips.methods.auth.login_options.LoginOptionsMixin.login_options`.
    Используется до аутентификации: выбрать роль/уровень и получить их числовые
    ``id`` для тела ``authenticate``, либо просто показать пользователю варианты
    входа. Оба списка могут быть пустыми (логин без назначенных ролей/уровней).

    Attributes:
        roles: Доступные роли (:class:`AuthRole`); пустой список, если ролей нет.
        access_levels: Доступные уровни доступа (:class:`AuthAccessLevel`);
            пустой список, если уровни не назначены.
    """

    roles: list[AuthRole] = Field(default_factory=list, description="Доступные роли")
    access_levels: list[AuthAccessLevel] = Field(
        default_factory=list, description="Доступные уровни доступа"
    )
