"""Добавление объекта IMBASE в папку избранного (обратимая запись)."""

from ...core import APIManager
from ...schemas.imbase.favorite_folder import FavoriteFolderDto


class ImBaseAddToFavoriteFolderMixin(APIManager):
    """Реализует ``POST .../favorites/{selectedFavoriteFolderId}/add/{objectId}``.

    operationId ``ImBase_AddToFavoriteFolder``.
    """

    async def imbase_add_to_favorite_folder(
        self: "ImBaseAddToFavoriteFolderMixin",
        favorite_folder_id: int,
        object_id: int,
    ) -> FavoriteFolderDto | None:
        """Добавляет объект в папку избранного IMBASE (личная закладка).

        Избранное — личная пользовательская навигация: закладки на объекты
        справочника поверх дерева. Метод помещает объект в указанную папку
        избранного и возвращает созданную связь-закладку. Запись ОБРАТИМА и НЕ
        мутирует сам объект — снимается парным методом
        :meth:`imbase_remove_from_favorites` (обратная пара add/remove).

        Когда применять: чтобы добавить объект в избранное пользователя. Оба
        параметра передаются в пути, тело запроса отсутствует. Идемпотентность не
        гарантируется сервером: повторное добавление — на стороне IPS.

        Args:
            favorite_folder_id: Идентификатор ПАПКИ избранного
                (``selectedFavoriteFolderId``, id-пространство папок избранного,
                НЕ ``ObjectID`` объекта), в которую кладём закладку.
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / ``ObjectID`` /
                F_OBJECT_ID, общий для версий), добавляемого в избранное.

        Returns:
            Связь-закладка по схеме :class:`FavoriteFolderDto` (``object_id``
            добавленного объекта, ``relation_id`` созданной закладки) либо ``None``.
            ⚠️ На обследованном билде IPS сервер при успешном добавлении отдаёт
            ``null`` (тело без содержимого), поэтому метод возвращает ``None`` —
            успех определяйте по отсутствию исключения, а факт закладки проверяйте
            через :meth:`imbase_favorite_folders_count` / список избранного.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                fav = await ips.imbase_add_to_favorite_folder(12, 102550)
                # позже — снять закладку (обратная операция):
                await ips.imbase_remove_from_favorites(12, 102550)

        Notes:
            operationId ``ImBase_AddToFavoriteFolder``; путь
            ``POST /core/api/imbase/favorites/{selectedFavoriteFolderId}/add/{objectId}``
            (без тела). Обратная операция — :meth:`imbase_remove_from_favorites`;
            счётчик папок — :meth:`imbase_favorite_folders_count`.
        """
        path = f"/core/api/imbase/favorites/{favorite_folder_id}/add/{object_id}"
        # Тела нет, но пустой ``json={}`` задаёт Content-Type application/json —
        # без него сервер отвечает 415 Unsupported Media Type (проверено на проде).
        data = await self._request("post", path, json={})
        # Сервер может вернуть ``null`` (без содержимого) при успешном добавлении.
        if not isinstance(data, dict):
            return None
        return FavoriteFolderDto.model_validate(data)
