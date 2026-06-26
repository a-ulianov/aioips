"""Метод перевода объекта в режим редактирования."""

from typing import Any

from ...core import APIManager


class ObjectEditMixin(APIManager):
    """Реализует ``POST /core/api/objects/{objectId}/edit`` (``Objects_Edit``)."""

    async def object_edit(
        self: "ObjectEditMixin",
        object_id: int,
        *,
        log_history: bool = True,
    ) -> None:
        """Переводит объект в режим редактирования (МУТИРУЮЩАЯ операция, меняет состояние).

        Универсальная точка входа в правку: сервер сам выбирает корректный режим
        модификации (in-base / checkout / createVersion) исходя из типа объекта и текущего
        шага его ЖЦ (см. :class:`~aioips.common.enumerations.ObjectModifyMode`). Применяйте,
        когда не хотите вручную решать между :meth:`object_check_out` и
        :meth:`object_create_object_version`. После правки фиксируйте :meth:`object_check_in`
        либо отменяйте :meth:`object_cancel_changes`.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``F_OBJECT_ID``), переводимого в правку — НЕ
                идентификатор версии.
            log_history: Журналировать ли операцию в истории модификаций
                (query ``isNeedToLogModificationHistory``).

        Returns:
            ``None`` — метод ничего не возвращает (тип ответа ``void``); состояние объекта
            на сервере меняется как побочный эффект.

        Raises:
            IPSConflictError: Если режим ЖЦ объекта не допускает редактирование либо объект
                уже извлечён другим пользователем.
            IPSError: При иной ошибке сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.object_edit(102550)
                await ips.object_set_attribute_values(102550, [...])
                await ips.object_check_in(102550)

        References:
            ``Objects_Edit``. Связанные: :meth:`object_check_out`,
            :meth:`object_create_object_version`, :meth:`object_cancel_changes`.
        """
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        await self._request("post", f"/core/api/objects/{object_id}/edit", json={}, params=params)
        return None
