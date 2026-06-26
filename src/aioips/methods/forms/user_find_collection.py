"""Метод форменного поиска пользователей по версиям (чтение через POST)."""

from ...core import APIManager
from ...schemas.forms.user import User


class UserFindCollectionMixin(APIManager):
    """Реализует ``POST /core/api/forms/userFindCollection``.

    operationId ``Forms_UserFindCollection``.
    """

    async def user_find_collection(
        self: "UserFindCollectionMixin",
        ids: list[int],
    ) -> list[User]:
        """Возвращает пользователей по списку версий (чтение через POST).

        По переданному списку версий отбирает соответствующих пользователей. Несмотря на
        HTTP-метод POST, это операция ЧТЕНИЯ: сервер ничего не изменяет, тело — голый
        JSON-массив идентификаторов.

        Когда применять: чтобы получить пользователей по их версиям (например, разрешить
        набор id в карточки пользователей). Родственные методы:
        :meth:`rank_find_collection` (ранги по версиям),
        :meth:`user_group_find_collection` (группы по версиям). В отличие от
        :meth:`find_users`, здесь источник — плоский список версий пользователей,
        без групп/рангов.

        Предусловие по id-пространству: ``ids`` — идентификаторы ВЕРСИЙ (F_ID), не
        объектов. См. [[ips-object-model]].

        Args:
            ids: Список идентификаторов ВЕРСИЙ пользователей (F_ID). Тело отправляется
                как голый JSON-массив ``list[int]``.

        Returns:
            Список пользователей по схеме :class:`User` (DTO ``UserDto`` / ``IEntityDto``).
            Пустой список — ничего не найдено по переданным версиям.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                users = await ips.user_find_collection([7001, 7002])
                print([u.caption for u in users])

        Notes:
            operationId ``Forms_UserFindCollection``; путь
            ``POST /core/api/forms/userFindCollection``; тело — голый ``list[int]``;
            ответ — массив ``UserDto`` (``IEntityDto``).
        """
        data = await self._request("post", "/core/api/forms/userFindCollection", json=ids)
        items = data if isinstance(data, list) else []
        return [User.model_validate(item) for item in items]
