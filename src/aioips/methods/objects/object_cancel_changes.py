"""Метод отмены несохранённых изменений объектов."""

from typing import Any

from ...core import APIManager


class ObjectCancelChangesMixin(APIManager):
    """Реализует ``POST /core/api/objects/cancelChanges`` (``Objects_CancelChanges``)."""

    async def object_cancel_changes(
        self: "ObjectCancelChangesMixin",
        object_ids: list[int],
        *,
        confirm: bool = False,
        admin_mode: bool | None = None,
        log_history: bool = True,
        ignore_exceptions: bool | None = None,
    ) -> list[int]:
        """Отменяет несохранённые правки объектов (МУТИРУЮЩАЯ; защищена ``confirm``).

        Откатывает рабочие копии к последнему зафиксированному состоянию и снимает блокировку
        редактирования — завершает цикл правки альтернативно :meth:`object_check_in`. Внесённые
        после checkout/edit изменения теряются БЕЗВОЗВРАТНО, поэтому по умолчанию метод НЕ
        выполняется: требуется явный ``confirm=True``, иначе поднимается :class:`ValueError`
        ещё до обращения к серверу.

        Предупреждение: убедитесь, что несохранённые изменения действительно не нужны —
        восстановить их после отмены нельзя.

        Args:
            object_ids: Идентификаторы ОБЪЕКТОВ (``F_OBJECT_ID``), правки которых отменяются
                (передаются телом запроса как ``list[int]``).
            confirm: Подтверждение разрушающей операции. Без ``True`` метод не делает запрос.
            admin_mode: Выполнять в административном режиме (query ``isAdminMode``); ``None`` —
                параметр не передаётся (серверный дефолт).
            log_history: Журналировать ли операцию в истории модификаций
                (query ``isNeedToLogModificationHistory``).
            ignore_exceptions: Игнорировать ошибки по отдельным объектам и продолжать
                (query ``isNeedToIgnoreExceptions``); ``None`` — не передаётся.

        Returns:
            Список идентификаторов объектов, для которых отмена выполнена; пустой список,
            если сервер ничего не вернул.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                cancelled = await ips.object_cancel_changes([102550], confirm=True)

        References:
            ``Objects_CancelChanges``. Связанные: :meth:`object_check_in`,
            :meth:`object_check_out`, :meth:`object_edit`.
        """
        if confirm is not True:
            raise ValueError(
                "Отмена изменений необратима: передайте confirm=True для подтверждения"
            )
        params: dict[str, Any] = {
            "isNeedToLogModificationHistory": str(log_history).lower(),
        }
        if admin_mode is not None:
            params["isAdminMode"] = str(admin_mode).lower()
        if ignore_exceptions is not None:
            params["isNeedToIgnoreExceptions"] = str(ignore_exceptions).lower()
        data = await self._request(
            "post", "/core/api/objects/cancelChanges", json=object_ids, params=params
        )
        result = data.get("result") if isinstance(data, dict) else None
        return [int(x) for x in result] if result else []
