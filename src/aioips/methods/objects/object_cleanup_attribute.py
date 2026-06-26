"""Метод очистки значений атрибута объекта."""

from typing import Any

from ...core import APIManager


class ObjectCleanupAttributeMixin(APIManager):
    """Реализует ``ObjectAttributes_CleanUpAttribute`` (очистка значений атрибута)."""

    async def object_cleanup_attribute(
        self: "ObjectCleanupAttributeMixin",
        object_id: int,
        attribute_id: int,
        *,
        confirm: bool = False,
        log_history: bool = True,
    ) -> None:
        """Очищает значения атрибута объекта (РАЗРУШАЮЩАЯ операция).

        Удаляет значения атрибута, оставляя сам атрибут у объекта (в отличие от
        :meth:`object_delete_attribute`, который удаляет атрибут целиком). Применяйте,
        когда нужно сбросить характеристику в «пусто», сохранив её определение.

        Это необратимая потеря данных, поэтому защищена confirm-гейтом: при
        ``confirm=False`` метод НЕ выполняет HTTP-запрос и сразу поднимает ``ValueError``.

        ПРЕДУСЛОВИЕ (жизненный цикл): очистка возможна, только если объект извлечён на
        редактирование (checkout). Этот метод НЕ делает checkout сам — это отдельная
        операция (``CheckOut`` → править → ``CheckIn``/``CancelChanges``). Если объект
        не в режиме редактирования, сервер вернёт ошибку (409 / конфликт ЖЦ).

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для
                всех версий. Не идентификатор версии (``id`` / F_ID).
            attribute_id: Идентификатор ТИПА атрибута, значения которого очистить.
            confirm: Гейт подтверждения необратимого действия. Должен быть ``True``,
                иначе метод не выполнит запрос и поднимет ``ValueError``.
            log_history: Если ``True`` (по умолчанию), сервер фиксирует изменение в
                журнале истории модификаций (query ``isNeedToLogModificationHistory``).

        Returns:
            ``None``. Сервер возвращает «ничего» (``Nothing``) в обёртке с журналом.

        Raises:
            ValueError: Если ``confirm`` не ``True`` (до выполнения запроса).
            IPSConflictError: Если объект не извлечён на редактирование (конфликт ЖЦ).
            IPSForbiddenError: При отсутствии прав на изменение атрибута.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                # Объект 102550 предварительно извлечён на редактирование (checkout).
                await ips.object_cleanup_attribute(102550, 12, confirm=True)

        Notes:
            ``operationId``: ``ObjectAttributes_CleanUpAttribute``. См. объектной модели IPS
            (раздел «Редактирование») и устав §7 (confirm-гейты). Связанные методы:
            :meth:`object_delete_attribute`, :meth:`object_set_attribute_values`.
        """
        if not confirm:
            raise ValueError("требуется confirm=True для очистки атрибута")
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        await self._request(
            "delete",
            f"/core/api/objects/{object_id}/attributes/{attribute_id}/cleanup",
            params=params,
        )
        return None
