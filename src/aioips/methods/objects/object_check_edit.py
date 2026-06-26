"""Метод проверки возможности правки атрибутов объекта (check-edit)."""

from ...core import APIManager


class ObjectCheckEditMixin(APIManager):
    """Реализует ``GET /core/api/objects/{objectId}/checkEdit``.

    Соответствует операции ``Objects_CheckEdit``.
    """

    async def object_check_edit(
        self: "ObjectCheckEditMixin",
        object_id: int,
    ) -> None:
        """Проверяет на сервере допустимость правки атрибутов объекта.

        Гейт-проверка прав/возможности изменить значения атрибутов объекта ПЕРЕД
        извлечением на редактирование (:meth:`object_check_out`). Сервер убеждается, что в
        текущем состоянии объекта (режим правки типа/шага ЖЦ, блокировки, права субъекта)
        правка атрибутов разрешена. Вызывайте, чтобы заранее отсеять недопустимый случай и
        не запускать цикл checkout → правка → checkIn впустую. Для проверки правки СВЯЗЕЙ
        (а не атрибутов) используйте :meth:`object_check_relations_edit`.

        Метод НИЧЕГО не возвращает: при допустимости правки — успешный ответ (``None``),
        при недопустимости — сервер отдаёт ошибку, которая поднимается как исключение. Сам
        по себе ничего не меняет (только чтение/проверка).

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии (F_ID).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), для которого
                проверяется допустимость правки атрибутов. Не идентификатор версии
                (``id`` / F_ID).

        Returns:
            ``None`` — метод ничего не возвращает (тип ответа ``void``). Успешное
            завершение означает, что правка атрибутов допустима.

        Raises:
            IPSError: Если правка атрибутов недопустима или при ином ошибочном ответе
                сервера (в т.ч. 403 при отсутствии прав, 404 если объект не найден).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.object_check_edit(102550)  # не бросило -> можно править
                working_id = await ips.object_check_out(102550)

        Notes:
            ``operationId``: ``Objects_CheckEdit``. Ответ без тела (``void``). Связанные
            методы: :meth:`object_check_out`, :meth:`object_check_relations_edit`,
            :meth:`object_set_attribute_values`. См. [[ips-object-model]] (раздел «Правка»).
        """
        await self._request("get", f"/core/api/objects/{object_id}/checkEdit")
        return None
