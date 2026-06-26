"""Метод удаления связи (мутирующий, разрушающий — защищён confirm-гейтом)."""

from typing import Any

from ...core import APIManager


class RelationDeleteMixin(APIManager):
    """Реализует ``DELETE /core/api/relations`` (``Relations_DeleteRelation``)."""

    async def relation_delete(
        self: "RelationDeleteMixin",
        relation_id: int,
        *,
        confirm: bool = False,
        delete_mode: int | None = None,
        log_history: bool = True,
    ) -> None:
        """Удаляет связь по её идентификатору (РАЗРУШАЮЩАЯ операция, защищена ``confirm``).

        Удаляет связь «родитель → потомок» (исключает объект из состава). Операция
        необратима, поэтому по умолчанию НЕ выполняется: требуется явный ``confirm=True``,
        иначе поднимается :class:`ValueError` ещё до обращения к серверу. Удаляется именно
        связь, а не объекты-концы. Для удаления отдельного атрибута связи используйте
        :meth:`relation_delete_attribute`.

        ПРЕДУСЛОВИЕ: объект-РОДИТЕЛЬ связи должен быть в режиме, разрешающем правку на
        текущем шаге ЖЦ (как правило — извлечён на редактирование, checkout). Внимание:
        ``relation_id`` нестабилен (меняется при checkout/checkin родителя), поэтому
        используйте свежий идентификатор, полученный непосредственно перед удалением.

        Args:
            relation_id: Идентификатор удаляемой СВЯЗИ (``relationID``, query ``relationId``;
                отдельное id-пространство связей). Не кэшируйте — нестабилен.
            confirm: Подтверждение разрушающей операции. Без ``True`` метод не делает
                запрос и поднимает :class:`ValueError`.
            delete_mode: Режим удаления/каскада (query ``deleteMode``). ``None`` — параметр
                не передаётся (поведение по умолчанию сервера).
            log_history: Если ``True`` (по умолчанию), сервер логирует историю
                модификаций (query ``isNeedToLogModificationHistory``); ``False`` — без
                журналирования.

        Returns:
            ``None``. Ответ-обёртка ``Nothing*`` не несёт полезной нагрузки; успех —
            отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSConflictError: Если связь нельзя удалить (блокировка/зависимости).
            IPSError: При иной ошибке сервера (в т.ч. если родитель не извлечён на
                редактирование).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.relation_delete(700123, confirm=True)

        Notes:
            ``operationId``: ``Relations_DeleteRelation``. Связанные:
            :meth:`relation_create`, :meth:`relation_delete_attribute`. Тело DELETE — ``{}``
            (на случай требования сервером ``Content-Type``). См. [[ips-object-model]].
        """
        if confirm is not True:
            raise ValueError("Удаление связи необратимо: передайте confirm=True для подтверждения")
        params: dict[str, Any] = {
            "relationId": str(relation_id),
            "isNeedToLogModificationHistory": str(log_history).lower(),
        }
        if delete_mode is not None:
            params["deleteMode"] = str(delete_mode)
        await self._request("delete", "/core/api/relations", json={}, params=params)
        return None
