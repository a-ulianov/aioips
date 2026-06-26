"""Метод поиска групп пользователей в составе формы."""

from typing import Any

from ...core import APIManager
from ...schemas.forms import UserGroup


class FindUserGroupsInCompositionMixin(APIManager):
    """Реализует ``GET /core/api/forms/findUserGroupsInComposition``.

    operationId ``Forms_FindUserGroupsInComposition``.
    """

    async def find_user_groups_in_composition(
        self: "FindUserGroupsInCompositionMixin",
        version_id: int,
    ) -> list[UserGroup]:
        """Возвращает группы пользователей, найденные в составе формы данной версии.

        Разбирает состав (композицию) формы и извлекает из него адресаты-группы
        пользователей. Применяется при работе с формами, где состав задаёт получателей
        прав или рассылок: метод даёт только группы, без раскрытия входящих в них
        пользователей.

        Предусловие по id-пространству (критично): аргумент — это идентификатор ВЕРСИИ
        объекта-формы (``versionID`` / F_ID, поле ``id`` в DTO версии), а НЕ идентификатор
        объекта (``objectID`` / F_OBJECT_ID). Передача id объекта вместо id версии вернёт
        пустой результат (см. объектной модели IPS, раздел «Идентичность»).

        Связанные методы: :meth:`rank_find_inner_users` (только пользователи состава),
        :meth:`find_user_groups_and_users` (группы и пользователи одним вызовом).

        Args:
            version_id: Идентификатор ВЕРСИИ объекта-формы (``versionID`` / F_ID),
                чей состав анализируется. Не идентификатор объекта (``objectID``).

        Returns:
            Список групп пользователей по схеме :class:`UserGroup`. Пустой список
            означает, что в составе формы нет групп (либо передан неверный id версии).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                groups = await ips.find_user_groups_in_composition(102551)
                for g in groups:
                    print(g.id, g.caption)

        Notes:
            operationId ``Forms_FindUserGroupsInComposition``; путь
            ``GET /core/api/forms/findUserGroupsInComposition`` (query ``versionId``);
            ответ — массив ``UserGroupDto`` (``IEntityDto``).
        """
        params: dict[str, Any] = {"versionId": version_id}
        data = await self._request(
            "get", "/core/api/forms/findUserGroupsInComposition", params=params
        )
        return [UserGroup.model_validate(item) for item in data]
