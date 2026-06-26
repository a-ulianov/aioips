"""Метод получения состава снимка объекта."""

from ...core import APIManager


class SnapshotCompositionMixin(APIManager):
    """Реализует ``GET /core/api/snapshots/{snapshotId}/composition``.

    operationId ``Snapshots_GetObjectSnapshotComposition``.
    """

    async def snapshot_composition(
        self: "SnapshotCompositionMixin",
        snapshot_id: int,
    ) -> list[int]:
        """Возвращает состав снимка объекта — список id версий вошедших в него элементов.

        Снимок (snapshot) — это зафиксированное на момент его создания состояние состава
        объекта: «замороженный» перечень версий элементов, которые входили в объект, когда
        снимок был сделан. В отличие от текущего состава, снимок не меняется со временем и
        служит исторической точкой отсчёта. Метод возвращает плоский список идентификаторов
        этих элементов.

        Предусловие по id-пространству (критично): аргумент ``snapshot_id`` — это
        идентификатор самого снимка, а элементы результата — это id ВЕРСИЙ (F_ID), а НЕ
        id объектов (F_OBJECT_ID). Чтобы загрузить объект по такому id через
        :meth:`object_get`, он не годится напрямую (``object_get`` принимает id объекта);
        см. объектной модели IPS (раздел «Идентичность»).

        Args:
            snapshot_id: Идентификатор снимка (int64), состав которого нужно получить.

        Returns:
            Список идентификаторов версий (int64) элементов, входящих в снимок. Пустой
            список означает, что снимок не содержит элементов (или снимок не найден).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                version_ids = await ips.snapshot_composition(45012)
                print(len(version_ids))  # число элементов в снимке

        Notes:
            operationId ``Snapshots_GetObjectSnapshotComposition``; путь
            ``GET /core/api/snapshots/{snapshotId}/composition``. Ответ — голый массив
            int64. Элементы — id версий (F_ID), не id объектов.
        """
        data = await self._request("get", f"/core/api/snapshots/{snapshot_id}/composition")
        return [int(item) for item in data]
