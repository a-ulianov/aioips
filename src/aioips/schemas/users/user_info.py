"""Схема информации о текущем пользователе сессии.

Описывает тело ``CurrentUserInfoDto`` — «кто я» для активной авторизованной
сессии: идентификатор сессии, активная роль и уровень доступа, признак
администратора, имена пользователя.

References:
    ``GET /core/api/currentUsers/userInfo`` — ``CurrentUserInfoDto``.
    Домен: разделу авторизации, объектной модели IPS.
"""

from uuid import UUID

from pydantic import Field

from ..base import IPSModel


class CurrentUserInfo(IPSModel):
    """Сведения о пользователе текущей авторизованной сессии («кто я»).

    Результат :meth:`~aioips.methods.users.user_info.UserInfoMixin.user_info`
    (``GET /core/api/currentUsers/userInfo``). Отражает уже выполненный вход:
    под какой ролью и уровнем доступа работает сессия и есть ли админ-права.
    JSON приходит в camelCase (``sessionId``, ``userVersionId``, ``roleVersionId``,
    ``accessLevel``, ``isAdmin``, ``loginName``, ``userName``); алиасы генерируются
    автоматически базовой моделью.

    Важно (различие версия/объект, см. объектной модели IPS): поля ``*_version_id``
    несут идентификаторы ВЕРСИЙ соответствующих объектов (F_ID), а не id объектов
    (F_OBJECT_ID); их нельзя напрямую подавать в методы, ожидающие ``objectID``.

    Attributes:
        session_id: UUID текущей сессии (``sessionId``).
        user_version_id: Идентификатор версии объекта пользователя (F_ID).
        user_name: Отображаемое имя пользователя; ``None``, если сервер не вернул.
        role_version_id: Идентификатор версии роли, под которой выполнен вход (F_ID).
        access_level: Идентификатор уровня доступа сессии (``accessLevelID``).
        is_admin: Признак административных прав (``True`` — администратор).
        login_name: Имя для входа (логин); ``None``, если сервер не вернул.
    """

    session_id: UUID = Field(description="Идентификатор сессии (sessionId)")
    user_version_id: int = Field(description="Идентификатор версии пользователя (F_ID)")
    user_name: str | None = Field(default=None, description="Отображаемое имя пользователя")
    role_version_id: int = Field(description="Идентификатор версии роли (F_ID)")
    access_level: int = Field(description="Идентификатор уровня доступа (accessLevelID)")
    is_admin: bool = Field(description="Признак административных прав")
    login_name: str | None = Field(default=None, description="Имя для входа (логин)")
