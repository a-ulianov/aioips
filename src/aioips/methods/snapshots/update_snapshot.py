"""Метод обновления снимка состава объекта."""

from ...core import APIManager
from ...schemas.snapshots import UpdateSnapshot


class UpdateSnapshotMixin(APIManager):
    """Реализует ``PUT /core/api/snapshots/{snapshotId}`` (``Snapshots_UpdateObjectSnapshot``)."""

    async def update_snapshot(
        self: "UpdateSnapshotMixin",
        snapshot_id: int,
        snapshot: UpdateSnapshot,
    ) -> None:
        """Обновляет существующий снимок состава объекта (мутирующая операция).

        Снимок (snapshot, «итерация») — это зафиксированный перечень версий
        элементов состава. Этот метод изменяет ранее созданный снимок: задаёт
        новое наименование и/или новый перечень версий элементов. Применять, когда
        нужно скорректировать сохранённую веху, не создавая новую; для создания
        используйте :meth:`create_snapshot`, для чтения состава —
        :meth:`snapshot_composition`.

        Предусловие по id-пространству (критично): ``snapshot_id`` — это
        идентификатор самого СНИМКА (``snapshotId``), полученный из
        :meth:`create_snapshot`. А ``snapshot.composition_object_version_ids`` —
        это id ВЕРСИЙ (F_ID) элементов состава, а НЕ id объектов (F_OBJECT_ID) и не
        id снимка. См. объектной модели IPS (раздел «Идентичность»).

        Args:
            snapshot_id: Идентификатор обновляемого снимка (``snapshotId``, int64).
            snapshot: Новые параметры снимка (:class:`UpdateSnapshot`): наименование,
                список id версий элементов состава и необязательное правило
                контекста. Сериализуется по точным ключам API; поля со значением
                ``None`` в тело не попадают.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void); успехом считается
            ответ без ошибки.

        Raises:
            IPSClientError: При некорректном запросе (400).
            IPSNotFoundError: Если снимок с указанным id не найден.
            IPSError: При иной ошибке сервера.

        Example:
            from aioips.schemas.snapshots import UpdateSnapshot

            async with IPSClient(config=config) as ips:
                await ips.update_snapshot(
                    9001,
                    UpdateSnapshot(
                        snapshot_name="Релиз 1.1",
                        composition_object_version_ids=[45012, 45013, 45014],
                    ),
                )

        References:
            ``Snapshots_UpdateObjectSnapshot``. Связанные: :meth:`create_snapshot`,
            :meth:`delete_snapshot`, :meth:`snapshot_composition`.
        """
        payload = snapshot.model_dump(mode="json", by_alias=True, exclude_none=True)
        await self._request("put", f"/core/api/snapshots/{snapshot_id}", json=payload)
        return None
