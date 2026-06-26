"""Метод фиксации изменений объекта командой (check-in command)."""

from typing import Any

from ...core import APIManager


class ObjectCheckInCommandMixin(APIManager):
    """Реализует ``.../objects/{objectId}/checkInCommand`` (``Objects_CheckInCommand``)."""

    async def object_check_in_command(
        self: "ObjectCheckInCommandMixin",
        object_id: int,
        *,
        preserve_working_copies: bool | None = None,
        log_history: bool = True,
    ) -> int:
        """Фиксирует изменения объекта командой check-in (МУТИРУЮЩАЯ операция).

        Командный вариант фиксации правок (ср. :meth:`object_check_in`): сохраняет внесённые
        в рабочую копию изменения как новое состояние объекта. Дополнительно умеет сохранять
        рабочие копии после фиксации (``preserve_working_copies``), что удобно для продолжения
        правки без повторного извлечения.

        Args:
            object_id: Идентификатор рабочей копии/объекта, фиксируемого после правки.
            preserve_working_copies: Сохранять ли рабочие копии после фиксации
                (query ``preserveWorkingCopies``); ``None`` — параметр не передаётся
                (серверный дефолт).
            log_history: Журналировать ли операцию в истории модификаций
                (query ``isNeedToLogModificationHistory``).

        Returns:
            Идентификатор результирующей версии объекта после фиксации (``0``, если сервер
            вернул пустой результат).

        Raises:
            IPSConflictError: Если объект не был извлечён на редактирование.
            IPSError: При иной ошибке сервера.

        Example:
            async with IPSClient(config=config) as ips:
                working_id = await ips.object_check_out(102550)
                await ips.object_set_attribute_values(working_id, [...])
                new_version = await ips.object_check_in_command(
                    working_id, preserve_working_copies=True
                )

        References:
            ``Objects_CheckInCommand``. Связанные: :meth:`object_check_in`,
            :meth:`object_check_out`.
        """
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        if preserve_working_copies is not None:
            params["preserveWorkingCopies"] = str(preserve_working_copies).lower()
        data = await self._request(
            "post", f"/core/api/objects/{object_id}/checkInCommand", json={}, params=params
        )
        result = data.get("result") if isinstance(data, dict) else None
        return int(result) if result is not None else 0
