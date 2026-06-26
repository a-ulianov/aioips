"""Схема совместного результата «группы и пользователи» состава формы IPS.

References:
    ``GET /core/api/forms/findUserGroupsAndUsersInComposition`` — ``UserGroupAndUserDto``.
"""

from typing import Annotated

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel
from .user import User
from .user_group import UserGroup


class UserGroupAndUser(IPSModel):
    """Совместный результат: группы и пользователи из состава формы (``UserGroupAndUserDto``).

    Объединяет в одном ответе обе категории адресатов состава формы: список групп
    (:class:`UserGroup`) и список пользователей (:class:`User`). Удобно, когда нужны
    одновременно и группы, и индивидуальные пользователи без двух раздельных вызовов.

    Когда применять: как результат :meth:`find_user_groups_and_users` — комбинированной
    замены пары :meth:`find_user_groups_in_composition` (только группы) и
    :meth:`rank_find_inner_users` (только пользователи). Оба списка независимы и могут
    быть пустыми.

    Оба поля — необязательные списки с дефолтом ``[]``; IPS может присылать ``null``
    вместо пустого массива, поэтому применён :data:`EmptyListIfNone`.

    Attributes:
        user_groups: Группы пользователей из состава формы (может быть пустым).
        users: Пользователи из состава формы (может быть пустым).
    """

    user_groups: Annotated[list[UserGroup], EmptyListIfNone] = Field(
        default_factory=list, description="Группы пользователей из состава формы"
    )
    users: Annotated[list[User], EmptyListIfNone] = Field(
        default_factory=list, description="Пользователи из состава формы"
    )
