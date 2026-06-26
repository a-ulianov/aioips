"""Метод форменного поиска групп пользователей по версиям (чтение через POST)."""

from ...core import APIManager
from ...schemas.forms.user_group import UserGroup


class UserGroupFindCollectionMixin(APIManager):
    """Реализует ``POST /core/api/forms/userGroupFindCollection``.

    operationId ``Forms_UserGroupFindCollection``.
    """

    async def user_group_find_collection(
        self: "UserGroupFindCollectionMixin",
        ids: list[int],
    ) -> list[UserGroup]:
        """Возвращает группы пользователей по списку версий (чтение через POST).

        По переданному списку версий отбирает соответствующие группы пользователей.
        Несмотря на HTTP-метод POST, это операция ЧТЕНИЯ: сервер ничего не изменяет,
        тело — голый JSON-массив идентификаторов.

        Когда применять: чтобы получить группы по их версиям (например, разрешить набор
        id в карточки групп). Родственные методы:
        :meth:`user_find_collection` (пользователи по версиям),
        :meth:`rank_find_collection` (ранги по версиям).

        Предусловие по id-пространству: ``ids`` — идентификаторы ВЕРСИЙ (F_ID), не
        объектов. См. [[ips-object-model]].

        Args:
            ids: Список идентификаторов ВЕРСИЙ групп пользователей (F_ID). Тело
                отправляется как голый JSON-массив ``list[int]``.

        Returns:
            Список групп по схеме :class:`UserGroup` (DTO ``UserGroupDto`` /
            ``IEntityDto``). Пустой список — ничего не найдено по переданным версиям.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                groups = await ips.user_group_find_collection([5001, 5002])
                print([g.caption for g in groups])

        Notes:
            operationId ``Forms_UserGroupFindCollection``; путь
            ``POST /core/api/forms/userGroupFindCollection``; тело — голый ``list[int]``;
            ответ — массив ``UserGroupDto`` (``IEntityDto``).
        """
        data = await self._request("post", "/core/api/forms/userGroupFindCollection", json=ids)
        items = data if isinstance(data, list) else []
        return [UserGroup.model_validate(item) for item in items]
