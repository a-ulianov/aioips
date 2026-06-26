"""Метод форменного поиска рангов по версиям (чтение через POST)."""

from ...core import APIManager
from ...schemas.forms.user import User


class RankFindCollectionMixin(APIManager):
    """Реализует ``POST /core/api/forms/rankFindCollection``.

    operationId ``Forms_RankFindCollection``.
    """

    async def rank_find_collection(
        self: "RankFindCollectionMixin",
        ids: list[int],
    ) -> list[User]:
        """Возвращает ранги (роли) по списку версий (чтение через POST).

        По переданному списку версий отбирает соответствующие ранги/роли. Несмотря на
        HTTP-метод POST, это операция ЧТЕНИЯ: сервер ничего не изменяет, тело — голый
        JSON-массив идентификаторов.

        Когда применять: чтобы получить ранги (роли) формы/назначений по их версиям —
        например, для отображения списка ролей. Родственные методы:
        :meth:`user_find_collection` (пользователи по версиям),
        :meth:`user_group_find_collection` (группы по версиям).

        Предусловие по id-пространству: ``ids`` — идентификаторы ВЕРСИЙ (F_ID), не
        объектов. См. объектной модели IPS.

        Args:
            ids: Список идентификаторов ВЕРСИЙ рангов (F_ID). Тело отправляется как
                голый JSON-массив ``list[int]``.

        Returns:
            Список рангов по схеме :class:`User` (DTO ``RankDto`` / ``IEntityDto`` —
            идентичность ``id``/``versionID``/``typeID``/``caption``). Пустой список —
            ничего не найдено по переданным версиям.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ranks = await ips.rank_find_collection([8001, 8002])
                print([r.caption for r in ranks])

        Notes:
            operationId ``Forms_RankFindCollection``; путь
            ``POST /core/api/forms/rankFindCollection``; тело — голый ``list[int]``;
            ответ — массив ``RankDto`` (структурно идентичен ``UserDto`` / ``IEntityDto``,
            поэтому переиспользуется схема :class:`User`).
        """
        data = await self._request("post", "/core/api/forms/rankFindCollection", json=ids)
        items = data if isinstance(data, list) else []
        return [User.model_validate(item) for item in items]
