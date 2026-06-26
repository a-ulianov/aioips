"""Метод создания новой версии объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import ObjectDto


class ObjectCreateObjectVersionMixin(APIManager):
    """Реализует ``.../CreateObjectVersion/{objectId}`` (``Objects_CreateObjectVersion``)."""

    async def object_create_object_version(
        self: "ObjectCreateObjectVersionMixin",
        object_id: int,
        *,
        log_history: bool = True,
    ) -> ObjectDto:
        """Создаёт новую версию объекта на основе текущей (МУТИРУЮЩАЯ операция).

        Порождает новую (рабочую) версию для объекта, чей тип/шаг ЖЦ требует режима
        ``createVersion`` (см. :class:`~aioips.common.enumerations.ObjectModifyMode`).
        В отличие от :meth:`object_check_out` (правка in-place той же версии), этот метод
        ветвит историю: предыдущая версия остаётся неизменной, а правка идёт по вновь
        созданной версии. Возвращённый объект уже находится в режиме редактирования —
        правьте его атрибуты, затем фиксируйте :meth:`object_check_in` либо отменяйте
        :meth:`object_cancel_changes`.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``F_OBJECT_ID``, общий для версий), для
                которого порождается новая версия — НЕ идентификатор конкретной версии.
            log_history: Журналировать ли операцию в истории модификаций
                (query ``isNeedToLogModificationHistory``).

        Returns:
            Новая (рабочая) версия объекта по схеме :class:`ObjectDto`; обычно с временным
            (отрицательным) ``id`` версии до фиксации.

        Raises:
            IPSConflictError: Если режим ЖЦ объекта не допускает создание версии.
            IPSError: При иной ошибке сервера.

        Example:
            async with IPSClient(config=config) as ips:
                draft = await ips.object_create_object_version(102550)
                await ips.object_set_attribute_values(draft.id, [...])
                await ips.object_check_in(draft.id)

        References:
            ``Objects_CreateObjectVersion``. Связанные: :meth:`object_check_out`,
            :meth:`object_check_in`, :meth:`object_cancel_changes`.
        """
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        data = await self._request(
            "post",
            f"/core/api/objects/CreateObjectVersion/{object_id}",
            json={},
            params=params,
        )
        result = data.get("result") if isinstance(data, dict) else None
        return ObjectDto.model_validate(result)
