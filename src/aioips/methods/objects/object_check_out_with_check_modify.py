"""Метод извлечения объекта на редактирование с проверкой модифицируемости."""

from typing import Any

from ...core import APIManager


class ObjectCheckOutWithCheckModifyMixin(APIManager):
    """Реализует ``.../checkOutWithCheckModify`` (``Objects_CheckOutWithCheckModify``)."""

    async def object_check_out_with_check_modify(
        self: "ObjectCheckOutWithCheckModifyMixin",
        object_id: int,
        *,
        log_history: bool = True,
    ) -> int:
        """Извлекает объект на редактирование с предварительной проверкой модифицируемости.

        Вариант :meth:`object_check_out`, который перед извлечением проверяет, допускает ли
        текущий тип и шаг ЖЦ изменение объекта (режим ``ObjectModifyModes``). Если правка
        запрещена (``cantModify``), сервер вернёт ошибку, не создавая рабочую копию. При
        успехе создаётся рабочая копия, и возвращается её идентификатор — **именно его**
        нужно передавать в методы записи (``object_set_attribute_values`` и др.), а НЕ
        идентификатор исходного объекта.

        После правки изменения фиксируются :meth:`object_check_in` (или
        :meth:`object_save_changes`) либо отменяются ``cancelChanges``.

        Args:
            object_id: Идентификатор объекта (``objectID``), извлекаемого на редактирование.
            log_history: Если ``True`` (по умолчанию), фиксировать операцию в журнале
                истории модификаций (query ``isNeedToLogModificationHistory``).

        Returns:
            Идентификатор рабочей копии (рабочая версия объекта), на которой выполняется
            правка. Обычно отрицательный (временный) до фиксации. ``0``, если сервер не
            вернул результат.

        Raises:
            IPSConflictError: Если объект уже извлечён другим пользователем либо режим ЖЦ
                не допускает редактирование (``cantModify``).
            IPSError: При иной ошибке сервера.

        Example:
            async with IPSClient(config=config) as ips:
                working_id = await ips.object_check_out_with_check_modify(102550)
                await ips.object_set_attribute_values(working_id, [...])
                await ips.object_check_in(working_id)

        References:
            ``Objects_CheckOutWithCheckModify``. Связанные: :meth:`object_check_out`,
            :meth:`object_check_in`, :meth:`object_save_changes`.
        """
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        data = await self._request(
            "post",
            f"/core/api/objects/{object_id}/checkOutWithCheckModify",
            json={},
            params=params,
        )
        result = data.get("result") if isinstance(data, dict) else None
        return int(result) if result is not None else 0
