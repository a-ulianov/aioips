"""Метод создания снимка состава объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.snapshots import CreateSnapshot


class CreateSnapshotMixin(APIManager):
    """Реализует ``POST /core/api/snapshots`` (``Snapshots_CreateObjectSnapshot``)."""

    async def create_snapshot(
        self: "CreateSnapshotMixin",
        snapshot: CreateSnapshot,
        *,
        object_id: int | None = None,
    ) -> int:
        """Создаёт новый снимок состава объекта и возвращает его идентификатор.

        Снимок (snapshot, «итерация») — это зафиксированное на момент создания
        состояние состава объекта: «замороженный» перечень версий элементов,
        который далее не меняется со временем и служит исторической точкой отсчёта.
        Этот метод — мутирующий: он создаёт такой снимок из явно перечисленных
        версий элементов состава и возвращает id нового снимка. Применять, когда
        нужно сохранить текущий (или произвольно собранный) состав как неизменяемую
        веху; прочитать состав снимка затем можно методом :meth:`snapshot_composition`.

        Предусловие по id-пространству (критично): в теле
        ``snapshot.composition_object_version_ids`` передаются идентификаторы
        ВЕРСИЙ (F_ID) элементов состава, а НЕ id объектов (F_OBJECT_ID). Возвращаемое
        значение — это id самого СНИМКА (``snapshotId``), которым затем оперируют
        :meth:`update_snapshot`, :meth:`delete_snapshot` и :meth:`snapshot_composition`.
        См. [[ips-object-model]] (раздел «Идентичность»).

        Args:
            snapshot: Параметры снимка (:class:`CreateSnapshot`): наименование,
                список id версий элементов состава и необязательное правило
                контекста. Сериализуется по точным ключам API; поля со значением
                ``None`` в тело не попадают.
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), для которого
                создаётся снимок (query-параметр ``objectId``). На практике обязателен:
                без него сервер отвечает 400 «объект N0 не найдено». ``None`` — параметр
                не передаётся.

        Returns:
            Идентификатор созданного снимка (``snapshotId``, int64). Ответ сервера —
            «голое» целое; при пустом теле ответа возвращается ``0``.

        Raises:
            IPSClientError: При некорректном запросе (400).
            IPSError: При иной ошибке сервера.

        Example:
            from aioips.schemas.snapshots import CreateSnapshot

            async with IPSClient(config=config) as ips:
                snapshot_id = await ips.create_snapshot(
                    CreateSnapshot(
                        snapshot_name="Релиз 1.0",
                        composition_object_version_ids=[45012, 45013],
                    )
                )
                print(snapshot_id)  # id нового снимка

        References:
            ``Snapshots_CreateObjectSnapshot``. Связанные: :meth:`update_snapshot`,
            :meth:`delete_snapshot`, :meth:`snapshot_composition`.
        """
        payload = snapshot.model_dump(mode="json", by_alias=True, exclude_none=True)
        params: dict[str, Any] = {}
        if object_id is not None:
            params["objectId"] = object_id
        data = await self._request("post", "/core/api/snapshots", json=payload, params=params)
        return int(data) if data is not None else 0
