"""Метод проверки возможности правки связей объекта."""

from ...core import APIManager


class ObjectCheckRelationsEditMixin(APIManager):
    """Реализует ``GET /core/api/objects/{objectId}/checkRelationsEdit``.

    Соответствует операции ``Objects_CheckRelationsEdit``.
    """

    async def object_check_relations_edit(
        self: "ObjectCheckRelationsEditMixin",
        object_id: int,
    ) -> None:
        """Проверяет на сервере допустимость правки связей объекта.

        Гейт-проверка перед изменением связей (состава/ссылок) объекта: сервер убеждается,
        что правка связей в текущем состоянии объекта разрешена (режим правки, блокировки,
        права). Вызывайте перед операциями, меняющими связи (например,
        :meth:`object_include_in_composition` / :meth:`object_exclude_from_composition` /
        :meth:`object_connect_to_object`), чтобы заранее отсеять недопустимый случай.
        Метод НИЧЕГО не возвращает: при допустимости правки — успешный ответ (``None``),
        при недопустимости — сервер отдаёт ошибку, которая поднимается как исключение.
        Сам по себе ничего не меняет (только чтение/проверка).

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии (F_ID).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), для которого
                проверяется допустимость правки связей. Не идентификатор версии
                (``id`` / F_ID).

        Returns:
            ``None`` — метод ничего не возвращает (тип ответа ``void``). Успешное
            завершение означает, что правка связей допустима.

        Raises:
            IPSError: Если правка связей недопустима или при ином ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.object_check_relations_edit(102550)  # не бросило -> можно править

        Notes:
            ``operationId``: ``Objects_CheckRelationsEdit``. Ответ без тела (``void``).
            Связанные методы: :meth:`object_include_in_composition`,
            :meth:`object_connect_to_object`.
        """
        await self._request("get", f"/core/api/objects/{object_id}/checkRelationsEdit")
        return None
