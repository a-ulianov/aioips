"""Метод получения хэша версии объекта."""

from ...core import APIManager


class ObjectHashVersionMixin(APIManager):
    """Реализует ``GET /core/api/objects/{objectId}/getHashVersion``.

    Соответствует операции ``Objects_GetHashVersion``.
    """

    async def object_hash_version(
        self: "ObjectHashVersionMixin",
        object_id: int,
    ) -> int:
        """Возвращает хэш версии объекта (целочисленный отпечаток состояния).

        Хэш версии — это числовой отпечаток текущего состояния версии объекта. Применяйте
        для дешёвой проверки, изменился ли объект между двумя чтениями (сравнить два хэша),
        и для оптимистичной блокировки/инвалидации кэша без загрузки всего объекта.
        Конкретный алгоритм — деталь сервера; сравнивайте хэши только на равенство, не
        интерпретируйте их величину. Только чтение — checkout не требуется.

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии (F_ID).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для всех
                версий. Не идентификатор версии (``id`` / F_ID).

        Returns:
            Целочисленный хэш версии объекта. Используется только для сравнения на
            равенство (одинаковый хэш ⇒ состояние не изменилось).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                before = await ips.object_hash_version(102550)
                # ... возможные изменения ...
                after = await ips.object_hash_version(102550)
                changed = before != after

        Notes:
            ``operationId``: ``Objects_GetHashVersion``. Ответ — голое целое
            (``type: integer``), не result-обёртка.
        """
        data = await self._request("get", f"/core/api/objects/{object_id}/getHashVersion")
        return int(data)
