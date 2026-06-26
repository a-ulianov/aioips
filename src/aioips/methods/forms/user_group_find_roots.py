"""Метод получения корневых групп пользователей."""

from ...core import APIManager
from ...schemas.forms import UserGroup


class UserGroupFindRootsMixin(APIManager):
    """Реализует ``GET /core/api/forms/userGroupFindRoots`` (``Forms_UserGroupFindRoots``)."""

    async def user_group_find_roots(
        self: "UserGroupFindRootsMixin",
    ) -> list[UserGroup]:
        """Возвращает корневые (верхнеуровневые) группы пользователей.

        Корни — это группы пользователей без родительской группы, то есть вершины
        иерархии групп. От них можно строить дерево групп вниз.

        Когда применять: чтобы получить отправную точку для навигации по иерархии
        групп пользователей (например, при построении дерева адресатов прав/рассылок).
        Параметры не требуются. Связанные методы: :meth:`find_user_groups_in_composition`
        (группы конкретной формы).

        Returns:
            Список корневых групп по схеме :class:`UserGroup`. Пустой список означает
            отсутствие групп верхнего уровня.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                roots = await ips.user_group_find_roots()
                for g in roots:
                    print(g.id, g.caption)

        Notes:
            operationId ``Forms_UserGroupFindRoots``; путь
            ``GET /core/api/forms/userGroupFindRoots``; ответ — массив ``UserGroupDto``.
        """
        data = await self._request("get", "/core/api/forms/userGroupFindRoots")
        return [UserGroup.model_validate(item) for item in data]
