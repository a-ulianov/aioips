"""Схема группы пользователей в составе формы IPS.

References:
    ``GET /core/api/forms/findUserGroupsInComposition`` — массив ``UserGroupDto``;
    также входит в ``UserGroupAndUserDto``. Базовый тип — ``IEntityDto``.
"""

from pydantic import Field

from ..base import IPSModel


class UserGroup(IPSModel):
    """Группа пользователей, найденная в составе формы (DTO ``UserGroupDto``).

    Лёгкое представление сущности-группы (``IEntityDto``): идентичность плюс заголовок
    и тип. Возвращается методами раздела forms, которые разбирают состав формы и
    извлекают из него адресатов-группы (например, для назначения прав или рассылок).

    Когда применять: при интерпретации результата
    :meth:`find_user_groups_in_composition` или поля ``user_groups`` структуры
    :class:`UserGroupAndUser`. Сами пользователи группы здесь не разворачиваются —
    их перечень по составу даёт :meth:`rank_find_inner_users`.

    Обязательно только поле идентичности ``id``. Прочие поля объявлены
    необязательными с дефолтами — это устойчиво к различиям между версиями API.

    Attributes:
        id: Идентификатор группы пользователей (``id`` в ``IEntityDto``).
        version_id: Идентификатор версии сущности (``versionID``); для групп обычно
            совпадает с ``id`` либо отсутствует.
        type_id: Идентификатор типа сущности (``typeID`` в метамодели IPS).
        caption: Заголовок (отображаемое имя) группы пользователей.
    """

    id: int = Field(description="Идентификатор группы пользователей")
    version_id: int | None = Field(
        default=None, alias="versionID", description="Идентификатор версии сущности"
    )
    type_id: int | None = Field(
        default=None, alias="typeID", description="Идентификатор типа сущности"
    )
    caption: str | None = Field(default=None, description="Заголовок группы пользователей")
