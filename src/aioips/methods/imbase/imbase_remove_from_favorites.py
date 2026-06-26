"""Удаление объекта IMBASE из избранного (обратная операция к add)."""

from ...core import APIManager


class ImBaseRemoveFromFavoritesMixin(APIManager):
    """Реализует ``POST .../favorites/{parentId}/remove/{objectId}``.

    operationId ``ImBase_RemoveFromFavorites``.
    """

    async def imbase_remove_from_favorites(
        self: "ImBaseRemoveFromFavoritesMixin",
        parent_id: int,
        object_id: int,
    ) -> None:
        """Удаляет объект из папки избранного IMBASE (обратная операция к add).

        Снимает личную закладку: убирает объект из указанной папки избранного.
        Это парная, ОБРАТНАЯ операция к :meth:`imbase_add_to_favorite_folder`
        (add/remove обратимы) и НЕ мутирует сам объект — затрагивается только
        личная навигация пользователя.

        Когда применять: чтобы убрать объект из избранного. Оба параметра в пути,
        тело запроса отсутствует. Ответ — пустой (``void``).

        Args:
            parent_id: Идентификатор ПАПКИ избранного (``parentId``, id-пространство
                папок избранного, НЕ ``ObjectID`` объекта), из которой удаляем
                закладку. Соответствует ``selectedFavoriteFolderId`` из add.
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / ``ObjectID`` /
                F_OBJECT_ID), снимаемого из избранного.

        Returns:
            ``None`` — сервер возвращает пустой ответ (``void``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.imbase_add_to_favorite_folder(12, 102550)
                await ips.imbase_remove_from_favorites(12, 102550)  # откат

        Notes:
            operationId ``ImBase_RemoveFromFavorites``; путь
            ``POST /core/api/imbase/favorites/{parentId}/remove/{objectId}`` (без
            тела, без содержимого в ответе). Обратная операция —
            :meth:`imbase_add_to_favorite_folder`.
        """
        path = f"/core/api/imbase/favorites/{parent_id}/remove/{object_id}"
        # Пустой ``json={}`` задаёт Content-Type application/json (иначе 415).
        await self._request("post", path, json={})
