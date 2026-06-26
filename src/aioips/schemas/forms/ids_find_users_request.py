"""Схема запроса поиска пользователей формы по идентификаторам IPS.

References:
    ``POST /core/api/forms/findUsers`` — тело запроса ``Ids4FindUsersRequest``.
"""

from typing import Annotated

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class Ids4FindUsersRequest(IPSModel):
    """Параметры поиска пользователей формы по идентификаторам (``Ids4FindUsersRequest``).

    Тело запроса для :meth:`forms_find_users`. Перечисляет источники адресатов —
    конкретных пользователей, группы пользователей и ранги (роли) — по их версиям; метод
    разворачивает их в плоский список пользователей.

    Предусловие по id-пространству (важно): все три списка содержат идентификаторы
    ВЕРСИЙ (F_ID / ``versionID``), не идентификаторы объектов. См. [[ips-object-model]].

    Все поля необязательны. Сериализуйте тело как ``model_dump(mode="json",
    by_alias=True, exclude_none=True)``.

    Attributes:
        user_version_ids: Версии пользователей (``userVersionIds``); ``null``
            нормализуется в пустой список.
        user_group_version_ids: Версии групп пользователей (``userGroupVersionIds``);
            ``null`` нормализуется в пустой список.
        rank_version_ids: Версии рангов/ролей (``rankVersionIds``); ``null``
            нормализуется в пустой список.
    """

    user_version_ids: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list,
        alias="userVersionIds",
        description="Версии пользователей",
    )
    user_group_version_ids: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list,
        alias="userGroupVersionIds",
        description="Версии групп пользователей",
    )
    rank_version_ids: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list,
        alias="rankVersionIds",
        description="Версии рангов/ролей",
    )
