"""Метод получения readonly-объектов снимка."""

from ...core import APIManager


class ObjectSnapshotReadonlyObjectsMixin(APIManager):
    """Реализует ``GET /core/api/objects/{objectId}/snapshots/{snapshotId}/info``.

    Соответствует операции ``Snapshots_GetSnapshotReadonlyObjects``.
    """

    async def object_snapshot_readonly_objects(
        self: "ObjectSnapshotReadonlyObjectsMixin",
        object_id: int,
        snapshot_id: int,
    ) -> list[int]:
        """Возвращает идентификаторы объектов, доступных только для чтения в снимке.

        Снимок (snapshot) фиксирует состояние состава объекта; часть входящих в него
        объектов зафиксирована и недоступна для правки (readonly). Метод возвращает список
        идентификаторов таких объектов для конкретного снимка. Применяйте, чтобы понять,
        какие элементы состава снимка нельзя изменять. Идентификаторы снимков узнавайте
        из :meth:`object_snapshot_info`. Только чтение.

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии (F_ID).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), которому
                принадлежит снимок. Не идентификатор версии (``id`` / F_ID).
            snapshot_id: Идентификатор снимка (``snapshot_id`` из
                :meth:`object_snapshot_info`).

        Returns:
            Список идентификаторов объектов, доступных только для чтения в данном снимке
            (возможно пустой, если таких объектов нет).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                info = await ips.object_snapshot_info(102550)
                if info.active_snapshot_id is not None:
                    ro = await ips.object_snapshot_readonly_objects(
                        102550, info.active_snapshot_id
                    )

        Notes:
            ``operationId``: ``Snapshots_GetSnapshotReadonlyObjects``. Ответ — голый
            массив целых (``array[int64]``), не result-обёртка. Связано с
            :meth:`object_snapshot_info`.
        """
        data = await self._request(
            "get", f"/core/api/objects/{object_id}/snapshots/{snapshot_id}/info"
        )
        return [int(item) for item in data] if isinstance(data, list) else []
