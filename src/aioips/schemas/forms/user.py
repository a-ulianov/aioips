"""Схема пользователя в составе формы IPS.

References:
    ``GET /core/api/forms/rankFindInnerUsersInComposition`` — массив ``UserDto``;
    также входит в ``UserGroupAndUserDto``. Базовый тип — ``IEntityDto``.
"""

from pydantic import Field

from ..base import IPSModel


class User(IPSModel):
    """Пользователь, найденный в составе формы (DTO ``UserDto``).

    Лёгкое представление сущности-пользователя (``IEntityDto``): идентичность плюс
    заголовок и тип. Возвращается методами раздела forms, которые разбирают состав
    формы и извлекают из него конкретных пользователей (в том числе входящих в группы).

    Когда применять: при интерпретации результата :meth:`rank_find_inner_users` или
    поля ``users`` структуры :class:`UserGroupAndUser`. Группы-адресаты возвращаются
    отдельно как :class:`UserGroup`.

    Обязательно только поле идентичности ``id``. Прочие поля объявлены
    необязательными с дефолтами — это устойчиво к различиям между версиями API.

    Attributes:
        id: Идентификатор пользователя (``id`` в ``IEntityDto``).
        version_id: Идентификатор версии сущности (``versionID``); для пользователей
            обычно совпадает с ``id`` либо отсутствует.
        type_id: Идентификатор типа сущности (``typeID`` в метамодели IPS).
        caption: Заголовок (отображаемое имя) пользователя.
    """

    id: int = Field(description="Идентификатор пользователя")
    version_id: int | None = Field(
        default=None, alias="versionID", description="Идентификатор версии сущности"
    )
    type_id: int | None = Field(
        default=None, alias="typeID", description="Идентификатор типа сущности"
    )
    caption: str | None = Field(default=None, description="Заголовок пользователя")
