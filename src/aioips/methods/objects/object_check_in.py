"""Метод фиксации изменений объекта (check-in)."""

from typing import Any

from ...core import APIManager


class ObjectCheckInMixin(APIManager):
    """Реализует ``POST /core/api/objects/{objectId}/checkIn`` (``Objects_CheckIn``)."""

    async def object_check_in(
        self: "ObjectCheckInMixin",
        object_id: int,
        *,
        log_history: bool = True,
    ) -> int:
        """Фиксирует изменения рабочей копии объекта и снимает блокировку редактирования.

        Завершает цикл правки, начатый :meth:`object_check_out`: сохраняет внесённые в
        рабочую копию изменения как новое состояние объекта и освобождает его. Чтобы
        сохранить изменения, не снимая блокировку, используйте :meth:`object_save_changes`;
        чтобы отменить — ``cancelChanges``.

        Args:
            object_id: Идентификатор рабочей копии (возвращённый :meth:`object_check_out`).
            log_history: Журналировать ли операцию в истории модификаций.

        Returns:
            Идентификатор результирующей версии объекта после фиксации.

        Raises:
            IPSConflictError: Если объект не был извлечён на редактирование.
            IPSError: При иной ошибке сервера.

        Example:
            async with IPSClient(config=config) as ips:
                working_id = await ips.object_check_out(102550)
                await ips.object_set_attribute_values(working_id, [...])
                await ips.object_check_in(working_id)

        References:
            ``Objects_CheckIn``. Связанные: :meth:`object_check_out`, :meth:`object_save_changes`.
        """
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        data = await self._request(
            "post", f"/core/api/objects/{object_id}/checkIn", json={}, params=params
        )
        result = data.get("result") if isinstance(data, dict) else None
        return int(result) if result is not None else 0
