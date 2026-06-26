"""Схема пользователя IPS Bridge.

References:
    ``GET /core/api/Bridge/UserInfo`` — ``BridgeUserDTO``.
"""

from pydantic import Field

from ..base import IPSModel


class BridgeUser(IPSModel):
    """Сведения о текущем пользователе моста IPS Bridge.

    Описывает пользователя, от имени которого работает IPS Bridge: его
    идентификатор, отображаемое имя, логин и идентификатор базы данных.
    Применяйте, чтобы определить активного пользователя клиентского моста
    (например, для подстановки в действия запуска или аудита).

    Attributes:
        id: Числовой идентификатор пользователя.
        user_name: Отображаемое имя пользователя в системе.
        login_name: Логин (имя входа) пользователя.
        database_id: Уникальный идентификатор базы данных.
    """

    id: int = Field(description="ID пользователя")
    user_name: str | None = Field(
        default=None, description="Отображаемое имя пользователя в системе"
    )
    login_name: str | None = Field(default=None, description="Логин пользователя")
    database_id: str | None = Field(default=None, description="Уникальный идентификатор БД")
