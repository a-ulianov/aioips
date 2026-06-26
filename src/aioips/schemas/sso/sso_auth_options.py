"""Схемы опций аутентификации Single Sign-On (Kerberos) пользователя IPS.

References:
    ``GET /core/api/sso/krb5/currentUser/options`` — ``SsoAuthOptionsDTO``.
"""

from typing import Annotated

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class AuthRole(IPSModel):
    """Роль пользователя IPS в составе опций аутентификации.

    Attributes:
        id: Идентификатор роли пользователя.
        name: Имя роли пользователя.
    """

    id: int = Field(description="Идентификатор роли пользователя")
    name: str = Field(description="Имя роли пользователя")


class AuthAccessLevel(IPSModel):
    """Уровень доступа пользователя IPS в составе опций аутентификации.

    Attributes:
        id: Идентификатор уровня доступа.
        name: Имя уровня доступа.
    """

    id: int = Field(description="Идентификатор уровня доступа")
    name: str = Field(description="Имя уровня доступа")


class AuthOptions(IPSModel):
    """Опции аутентификации пользователя IPS (соответствует ``AuthOptionsDTO``).

    Содержит наборы ролей и уровней доступа, доступных пользователю. Используется как
    вложенная структура ``login_options`` в :class:`SsoAuthOptions`.

    Списки роли/уровни доступа в swagger помечены непустыми (``minItems: 1``), но здесь
    смягчены до возможно пустых с дефолтом — это устойчиво к различиям версий API и
    отсутствию данных, а ``null`` приводится к пустому списку.

    Attributes:
        roles: Роли пользователя IPS.
        access_levels: Уровни доступа пользователя IPS.
    """

    roles: Annotated[list[AuthRole], EmptyListIfNone] = Field(
        default_factory=list, description="Роли пользователя IPS"
    )
    access_levels: Annotated[list[AuthAccessLevel], EmptyListIfNone] = Field(
        default_factory=list, description="Уровни доступа пользователя IPS"
    )


class SsoAuthOptions(IPSModel):
    """Опции аутентификации пользователя IPS для Single Sign-On (``SsoAuthOptionsDTO``).

    Возвращается при успешной аутентификации текущего пользователя по SPNEGO/Kerberos и
    описывает, под каким именем входа пользователь распознан и какие роли и уровни
    доступа ему доступны. Источник — :meth:`kerberos_auth_options`.

    Attributes:
        login_name: Имя входа пользователя IPS (обязательное поле).
        login_options: Опции аутентификации (роли и уровни доступа) — :class:`AuthOptions`.
    """

    login_name: str = Field(description="Имя входа пользователя IPS")
    login_options: AuthOptions = Field(
        description="Опции аутентификации пользователя IPS (роли и уровни доступа)"
    )
