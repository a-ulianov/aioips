"""Метод извлечения объекта на редактирование (check-out)."""

from typing import Any

from ...core import APIManager


class ObjectCheckOutMixin(APIManager):
    """Реализует ``POST /core/api/objects/{objectId}/checkOut`` (``Objects_CheckOut``)."""

    async def object_check_out(
        self: "ObjectCheckOutMixin",
        object_id: int,
        *,
        log_history: bool = True,
    ) -> int:
        """Извлекает объект на редактирование и возвращает id его рабочей копии.

        В IPS изменять атрибуты/связи объекта можно только после извлечения его на
        редактирование (check-out), если тип/шаг ЖЦ требует режима ``checkout`` (см.
        :class:`~aioips.common.enumerations.ObjectModifyMode`). Метод создаёт рабочую
        копию и возвращает её идентификатор — **именно его** нужно передавать в методы
        записи (``object_set_attribute_values``, ``object_set_attributes`` и др.), а НЕ
        идентификатор исходного объекта (иначе сервер вернёт 400).

        После правки изменения фиксируются :meth:`object_check_in` (или
        :meth:`object_save_changes`) либо отменяются ``cancelChanges``.

        Args:
            object_id: Идентификатор объекта (``objectID``), извлекаемого на редактирование.
            log_history: Журналировать ли операцию в истории модификаций.

        Returns:
            Идентификатор рабочей копии (рабочая версия объекта), на которой выполняется
            правка. Обычно отрицательный (временный) до фиксации.

        Raises:
            IPSConflictError: Если объект уже извлечён другим пользователем или режим ЖЦ
                не допускает редактирование.
            IPSError: При иной ошибке сервера.

        Example:
            async with IPSClient(config=config) as ips:
                working_id = await ips.object_check_out(102550)
                await ips.object_set_attribute_values(working_id, [...])
                await ips.object_check_in(working_id)

        References:
            ``Objects_CheckOut``. Связанные: :meth:`object_check_in`,
            :meth:`object_save_changes`, :meth:`object_set_attribute_values`.
        """
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        data = await self._request(
            "post", f"/core/api/objects/{object_id}/checkOut", json={}, params=params
        )
        result = data.get("result") if isinstance(data, dict) else None
        return int(result) if result is not None else 0
