"""Метод удаления атрибута объекта."""

from typing import Any

from ...core import APIManager


class ObjectDeleteAttributeMixin(APIManager):
    """Реализует ``ObjectAttributes_DeleteAttribute`` (удаление атрибута объекта)."""

    async def object_delete_attribute(
        self: "ObjectDeleteAttributeMixin",
        object_id: int,
        attribute_id: int,
        *,
        confirm: bool = False,
        log_history: bool = True,
    ) -> None:
        """Удаляет атрибут объекта (РАЗРУШАЮЩАЯ операция).

        Полностью удаляет атрибут (и все его значения) у объекта. Применяйте, когда
        характеристика больше не нужна. Чтобы лишь очистить значения, сохранив сам
        атрибут, используйте :meth:`object_cleanup_attribute`.

        Это необратимая операция, поэтому защищена confirm-гейтом: при ``confirm=False``
        метод НЕ выполняет HTTP-запрос и сразу поднимает ``ValueError``.

        ПРЕДУСЛОВИЕ (жизненный цикл): удаление возможно, только если объект извлечён на
        редактирование (checkout). Этот метод НЕ делает checkout сам — это отдельная
        операция (``CheckOut`` → править → ``CheckIn``/``CancelChanges``). Если объект
        не в режиме редактирования, сервер вернёт ошибку (409 / конфликт ЖЦ).

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для
                всех версий. Не идентификатор версии (``id`` / F_ID).
            attribute_id: Идентификатор ТИПА атрибута (какую характеристику удалить).
            confirm: Гейт подтверждения необратимого действия. Должен быть ``True``,
                иначе метод не выполнит запрос и поднимет ``ValueError``.
            log_history: Если ``True`` (по умолчанию), сервер фиксирует изменение в
                журнале истории модификаций (query ``isNeedToLogModificationHistory``).

        Returns:
            ``None``. Сервер возвращает «ничего» (``Nothing``) в обёртке с журналом.

        Raises:
            ValueError: Если ``confirm`` не ``True`` (до выполнения запроса).
            IPSConflictError: Если объект не извлечён на редактирование (конфликт ЖЦ).
            IPSForbiddenError: При отсутствии прав на удаление атрибута.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                # Объект 102550 предварительно извлечён на редактирование (checkout).
                await ips.object_delete_attribute(102550, 12, confirm=True)

        Notes:
            ``operationId``: ``ObjectAttributes_DeleteAttribute``. См. [[ips-object-model]]
            (раздел «Редактирование») и устав §7 (confirm-гейты). Связанные методы:
            :meth:`object_cleanup_attribute`, :meth:`object_set_attribute_values`.
        """
        if not confirm:
            raise ValueError("требуется confirm=True для удаления атрибута")
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        await self._request(
            "delete",
            f"/core/api/objects/{object_id}/attributes/{attribute_id}",
            params=params,
        )
        return None
