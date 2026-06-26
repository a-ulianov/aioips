"""Метод получения информации о снимках объекта."""

from ...core import APIManager
from ...schemas.objects import SnapshotInfo


class ObjectSnapshotInfoMixin(APIManager):
    """Реализует ``GET /core/api/objects/{objectId}/snapshots/info``.

    Соответствует операции ``Snapshots_GetObjectSnapshotInfo``.
    """

    async def object_snapshot_info(
        self: "ObjectSnapshotInfoMixin",
        object_id: int,
    ) -> SnapshotInfo:
        """Возвращает сводку по снимкам объекта: активный снимок и их коллекцию.

        Снимок (snapshot) — зафиксированное состояние объекта (обычно состава) на момент
        времени; у объекта может быть несколько снимков и один активный. Метод отдаёт
        идентификатор активного снимка и список всех снимков объекта. Применяйте, чтобы
        узнать, какие снимки доступны и какой активен, прежде чем читать состав снимка или
        его readonly-объекты (:meth:`object_snapshot_readonly_objects`). Только чтение.

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии (F_ID).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для всех
                версий. Не идентификатор версии (``id`` / F_ID).

        Returns:
            :class:`SnapshotInfo`: ``active_snapshot_id`` — id активного снимка (``None``,
            если активного нет), ``object_snapshot_collection`` — список снимков
            (:class:`ObjectSnapshot` с полями ``snapshot_id`` и ``name``; пустой, если
            снимков нет).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                info = await ips.object_snapshot_info(102550)
                print(info.active_snapshot_id)
                for snap in info.object_snapshot_collection:
                    print(snap.snapshot_id, snap.name)

        Notes:
            ``operationId``: ``Snapshots_GetObjectSnapshotInfo``. Ответ — объект
            ``SnapshotInfoDto`` (не result-обёртка). Связано с
            :meth:`object_snapshot_readonly_objects`.
        """
        data = await self._request("get", f"/core/api/objects/{object_id}/snapshots/info")
        return SnapshotInfo.model_validate(data)
