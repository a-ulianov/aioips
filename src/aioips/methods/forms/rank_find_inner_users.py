"""Метод поиска пользователей в составе формы (с учётом групп)."""

from typing import Any

from ...core import APIManager
from ...schemas.forms import User


class RankFindInnerUsersMixin(APIManager):
    """Реализует ``GET /core/api/forms/rankFindInnerUsersInComposition``.

    operationId ``Forms_RankFindInnerUsersInComposition``.
    """

    async def rank_find_inner_users(
        self: "RankFindInnerUsersMixin",
        version_id: int,
    ) -> list[User]:
        """Возвращает пользователей из состава формы, включая входящих в группы.

        Разбирает состав (композицию) формы и извлекает конкретных пользователей-адресатов.
        В отличие от :meth:`find_user_groups_in_composition` (только группы), этот метод
        раскрывает группы во внутренних (inner) пользователей: результат — плоский список
        пользователей, пригодный для адресной рассылки или назначения прав.

        Предусловие по id-пространству (критично): аргумент — это идентификатор ВЕРСИИ
        объекта-формы (``versionID`` / F_ID, поле ``id`` в DTO версии), а НЕ идентификатор
        объекта (``objectID`` / F_OBJECT_ID). Передача id объекта вернёт пустой результат
        (см. объектной модели IPS, раздел «Идентичность»).

        Связанные методы: :meth:`find_user_groups_in_composition` (только группы),
        :meth:`find_user_groups_and_users` (группы и пользователи одним вызовом).

        Args:
            version_id: Идентификатор ВЕРСИИ объекта-формы (``versionID`` / F_ID),
                чей состав анализируется. Не идентификатор объекта (``objectID``).

        Returns:
            Список пользователей по схеме :class:`User`. Пустой список означает, что в
            составе формы нет пользователей (либо передан неверный id версии).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                users = await ips.rank_find_inner_users(102551)
                print([u.caption for u in users])

        Notes:
            operationId ``Forms_RankFindInnerUsersInComposition``; путь
            ``GET /core/api/forms/rankFindInnerUsersInComposition`` (query ``versionId``);
            ответ — массив ``UserDto`` (``IEntityDto``).
        """
        params: dict[str, Any] = {"versionId": version_id}
        data = await self._request(
            "get", "/core/api/forms/rankFindInnerUsersInComposition", params=params
        )
        return [User.model_validate(item) for item in data]
