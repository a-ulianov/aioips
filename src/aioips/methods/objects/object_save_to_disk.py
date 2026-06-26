"""Метод выгрузки файлов объекта на диск."""

from ...core import APIManager


class ObjectSaveToDiskMixin(APIManager):
    """Реализует ``Objects_SaveToDisk`` (сохранение объекта на диск)."""

    async def object_save_to_disk(
        self: "ObjectSaveToDiskMixin",
        object_id: int,
    ) -> None:
        """Сохраняет файлы (blob-атрибуты) объекта на диск средствами сервера.

        Запускает серверную операцию выгрузки связанных с объектом файлов из
        хранилища (vault) в файловую систему по настроенным правилам. Метод не
        возвращает путь/содержимое — только подтверждает приём операции без ошибки.
        Применяйте для программной выгрузки документов так же, как из UI.

        Предусловие по id-пространству: ``object_id`` — это ``objectID``
        (F_OBJECT_ID), общий для всех версий, а НЕ ``id`` версии (F_ID).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), файлы
                которого выгружаются на диск. Не идентификатор версии.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.object_save_to_disk(102550)

        Notes:
            ``operationId``: ``Objects_SaveToDisk``. Эндпоинт
            ``POST /core/api/objects/{objectId}/saveToDisk``. Тело пустое (``{}``);
            ответ — void → ``None``. Связанный метод: :meth:`object_save_to_arc_copy`.
        """
        await self._request("post", f"/core/api/objects/{object_id}/saveToDisk", json={})
        return None
