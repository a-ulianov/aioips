"""Метод получения числа папок «Избранное», содержащих объект IMBASE."""

from ...core import APIManager


class ImBaseFavoriteFoldersCountMixin(APIManager):
    """Реализует ``GET /core/api/imbase/object/{objectId}/favoriteFoldersCount``."""

    async def imbase_favorite_folders_count(
        self: "ImBaseFavoriteFoldersCountMixin",
        object_id: int,
    ) -> int:
        """Возвращает число папок «Избранное», в которые добавлен объект IMBASE.

        Показывает, в скольких персональных папках «Избранное» присутствует данный
        объект справочной системы. Применяется в UI (значок/счётчик избранного,
        решение о показе кнопки удаления из избранного). Ответ — целое число.

        Когда применять: чтобы отобразить состояние «в избранном» для записи IMBASE.
        ``0`` означает, что объект не добавлен ни в одну папку избранного.

        Args:
            object_id: Идентификатор объекта IMBASE (id-пространство объектов IMBASE).

        Returns:
            Количество папок «Избранное», содержащих объект (``int``, ``>= 0``).
            Сервер не возвращает ``None``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                count = await ips.imbase_favorite_folders_count(123456)
                print("в избранном:", count)

        Notes:
            operationId ``ImBase_GetFavoriteFoldersCount``; путь
            ``GET /core/api/imbase/object/{objectId}/favoriteFoldersCount``
            (возвращает ``int32``).
        """
        data = await self._request(
            "get", f"/core/api/imbase/object/{object_id}/favoriteFoldersCount"
        )
        return int(data)
