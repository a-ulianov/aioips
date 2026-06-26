"""Метод форменного поиска пользователей по идентификаторам (чтение через POST)."""

from ...core import APIManager
from ...schemas.forms.ids_find_users_request import Ids4FindUsersRequest
from ...schemas.forms.user import User


class FindUsersMixin(APIManager):
    """Реализует ``POST /core/api/forms/findUsers``.

    operationId ``Forms_FindUsers``.
    """

    async def find_users(
        self: "FindUsersMixin",
        request: Ids4FindUsersRequest,
    ) -> list[User]:
        """Разворачивает источники адресатов в список пользователей (чтение через POST).

        По переданным версиям пользователей, групп пользователей и рангов (ролей)
        возвращает плоский список конкретных пользователей. Несмотря на HTTP-метод POST,
        это операция ЧТЕНИЯ: сервер ничего не изменяет, тело служит контейнером
        идентификаторов-источников.

        Когда применять: чтобы из смешанного набора адресатов (пользователи + группы +
        ранги) получить итоговый перечень реальных пользователей — например, для адресной
        рассылки или назначения прав. Аналог по составу формы —
        :meth:`rank_find_inner_users` (но тот принимает одну версию формы).

        Предусловие по id-пространству (см. :class:`Ids4FindUsersRequest`): все три списка
        — идентификаторы ВЕРСИЙ (F_ID), не объектов.

        Args:
            request: Параметры запроса (:class:`Ids4FindUsersRequest`): версии
                пользователей, групп и рангов-источников.

        Returns:
            Список пользователей по схеме :class:`User` (DTO ``UserDto`` / ``IEntityDto``).
            Пустой список — источники не дали ни одного пользователя.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                req = Ids4FindUsersRequest(user_group_version_ids=[5002], rank_version_ids=[8001])
                users = await ips.find_users(req)
                print([u.caption for u in users])

        Notes:
            operationId ``Forms_FindUsers``; путь ``POST /core/api/forms/findUsers``;
            тело — ``Ids4FindUsersRequest``; ответ — массив ``UserDto`` (``IEntityDto``).
        """
        payload = request.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/forms/findUsers", json=payload)
        items = data if isinstance(data, list) else []
        return [User.model_validate(item) for item in items]
