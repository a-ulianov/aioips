"""Метод сохранения изменений объекта без снятия блокировки."""

from typing import Any

from ...core import APIManager


class ObjectSaveChangesMixin(APIManager):
    """Реализует ``POST /core/api/objects/{objectId}/saveChanges`` (``Objects_SaveChanges``)."""

    async def object_save_changes(
        self: "ObjectSaveChangesMixin",
        object_id: int,
        *,
        log_history: bool = True,
    ) -> None:
        """Сохраняет изменения извлечённого объекта, НЕ снимая блокировку редактирования.

        Применяется внутри открытого цикла правки (после :meth:`object_check_out`), когда
        нужно зафиксировать промежуточные изменения, но продолжить редактирование. Чтобы
        завершить правку и освободить объект, используйте :meth:`object_check_in`.

        Args:
            object_id: Идентификатор рабочей копии (из :meth:`object_check_out`).
            log_history: Журналировать ли операцию в истории модификаций.

        Returns:
            ``None``. Успех подтверждается отсутствием исключения.

        Raises:
            IPSConflictError: Если объект не извлечён на редактирование.
            IPSError: При иной ошибке сервера.

        Example:
            async with IPSClient(config=config) as ips:
                working_id = await ips.object_check_out(102550)
                await ips.object_set_attribute_values(working_id, [...])
                await ips.object_save_changes(working_id)  # сохранить, остаться в правке

        References:
            ``Objects_SaveChanges``. Связанные: :meth:`object_check_out`, :meth:`object_check_in`.
        """
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        await self._request(
            "post", f"/core/api/objects/{object_id}/saveChanges", json={}, params=params
        )
