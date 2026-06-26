"""Метод удаления снимка состава объекта."""

from ...core import APIManager


class DeleteSnapshotMixin(APIManager):
    """Реализует ``DELETE /core/api/snapshots/{snapshotId}``.

    operationId ``Snapshots_DeleteObjectSnapshot``.
    """

    async def delete_snapshot(
        self: "DeleteSnapshotMixin",
        snapshot_id: int,
        *,
        confirm: bool = False,
    ) -> None:
        """Удаляет снимок состава объекта (РАЗРУШАЮЩАЯ операция, защищена ``confirm``).

        Снимок (snapshot, «итерация») — это зафиксированный, исторически значимый
        перечень версий элементов состава. Удаление снимка необратимо: восстановить
        его потом нельзя. Поэтому по умолчанию метод НЕ выполняется — требуется явный
        ``confirm=True``, иначе поднимается :class:`ValueError` ещё до обращения к
        серверу. Удаляется только сам снимок (веха состава); версии элементов,
        которые в него входили, не затрагиваются. Для создания снимка см.
        :meth:`create_snapshot`, для чтения его состава — :meth:`snapshot_composition`.

        Предусловие по id-пространству (критично): ``snapshot_id`` — это
        идентификатор самого СНИМКА (``snapshotId``), полученный из
        :meth:`create_snapshot`, а НЕ id объекта и не id версии элемента состава.
        См. [[ips-object-model]] (раздел «Идентичность»).

        Args:
            snapshot_id: Идентификатор удаляемого снимка (``snapshotId``, int64).
            confirm: Подтверждение разрушающей операции. Без ``True`` метод не
                делает запрос и поднимает :class:`ValueError` (защитный гейт).

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void); успехом считается
            ответ без ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSNotFoundError: Если снимок с указанным id не найден.
            IPSError: При иной ошибке сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.delete_snapshot(9001, confirm=True)

        References:
            ``Snapshots_DeleteObjectSnapshot``. Связанные: :meth:`create_snapshot`,
            :meth:`update_snapshot`, :meth:`snapshot_composition`.
        """
        if confirm is not True:
            raise ValueError("Удаление снимка необратимо: передайте confirm=True для подтверждения")
        # json={} — на случай, если сервер отвергает запрос без тела с 415.
        await self._request("delete", f"/core/api/snapshots/{snapshot_id}", json={})
        return None
