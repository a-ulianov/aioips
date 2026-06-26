"""Метод совместного поиска групп и пользователей в составе формы (явный путь)."""

from typing import Any

from ...core import APIManager
from ...schemas.forms import UserGroupAndUser


class FindUserGroupsAndUsersInCompositionMixin(APIManager):
    """Реализует ``GET /core/api/forms/findUserGroupsAndUsersInComposition``.

    operationId ``Forms_FindUserGroupsAndUsersInComposition``.
    """

    async def find_user_groups_and_users_in_composition(
        self: "FindUserGroupsAndUsersInCompositionMixin",
        version_id: int,
    ) -> UserGroupAndUser:
        """Возвращает группы и пользователей состава формы одним вызовом.

        Комбинированный разбор состава (композиции) формы: в одном ответе обе категории
        адресатов — группы (:class:`UserGroup`) и пользователи (:class:`User`).

        Предусловие по id-пространству (критично): аргумент — идентификатор ВЕРСИИ
        объекта-формы (``versionID`` / F_ID), а НЕ идентификатор объекта (``objectID`` /
        F_OBJECT_ID). Передача id объекта вернёт пустые списки
        (см. объектной модели IPS, раздел «Идентичность»).

        Когда применять: когда нужны и группы, и пользователи состава формы сразу,
        без двух раздельных вызовов. Близкий метод-обёртка с тем же поведением —
        :meth:`find_user_groups_and_users`.

        Args:
            version_id: Идентификатор ВЕРСИИ объекта-формы (``versionID`` / F_ID),
                чей состав анализируется. Не идентификатор объекта (``objectID``).

        Returns:
            Структура :class:`UserGroupAndUser` с полями ``user_groups`` и ``users``.
            Оба списка независимы и могут быть пустыми (в т.ч. при неверном id версии).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                result = await ips.find_user_groups_and_users_in_composition(102551)
                print(len(result.user_groups), len(result.users))

        Notes:
            operationId ``Forms_FindUserGroupsAndUsersInComposition``; путь
            ``GET /core/api/forms/findUserGroupsAndUsersInComposition`` (query
            ``versionId``); ответ — объект ``UserGroupAndUserDto``.
        """
        params: dict[str, Any] = {"versionId": version_id}
        data = await self._request(
            "get", "/core/api/forms/findUserGroupsAndUsersInComposition", params=params
        )
        return UserGroupAndUser.model_validate(data)
