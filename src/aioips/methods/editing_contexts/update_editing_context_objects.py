"""Метод обновления версий объектов в контексте редактирования."""

from ...core import APIManager
from ...schemas.editing_contexts import UpdateEditingContextObjectsIn


class UpdateEditingContextObjectsMixin(APIManager):
    """Реализует ``EditingContexts_UpdateEditingContextObjectsIn`` (обновление объектов)."""

    async def update_editing_context_objects(
        self: "UpdateEditingContextObjectsMixin",
        editing_context_id: int,
        body: UpdateEditingContextObjectsIn,
    ) -> None:
        """Обновляет версии объектов в контексте редактирования (МУТИРУЮЩАЯ операция).

        Контекст редактирования — это рабочий набор версий объектов для совместной
        правки. Метод приводит перечисленные версии объектов контекста к актуальному
        состоянию (обновляет их в составе контекста).

        Когда применять: для массового обновления уже входящих в контекст объектов.
        Для точечной подмены одной версии на другую используйте
        :meth:`replace_version_in_editing_context`.

        Предусловия по id-пространству: ``editing_context_id`` — идентификатор контекста
        редактирования; ``object_version_ids`` в теле — это ``id`` ВЕРСИЙ объектов
        (F_ID), а не ``objectID`` объектов.

        Args:
            editing_context_id: Идентификатор контекста редактирования (подставляется
                в путь ``{editingContextId}``).
            body: Тело запроса :class:`UpdateEditingContextObjectsIn` — список ``id``
                версий объектов, подлежащих обновлению.

        Returns:
            ``None``. Сервер не возвращает содержательного тела (void).

        Raises:
            IPSForbiddenError: При отсутствии прав на изменение контекста.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            from aioips.schemas.editing_contexts import UpdateEditingContextObjectsIn

            async with IPSClient(config=config) as ips:
                await ips.update_editing_context_objects(
                    501,
                    UpdateEditingContextObjectsIn(object_version_ids=[102550, 102551]),
                )

        Notes:
            ``operationId``: ``EditingContexts_UpdateEditingContextObjectsIn``; путь
            ``POST /core/api/editingContexts/{editingContextId}/update``. Связанные
            методы: :meth:`add_objects_to_editing_context`,
            :meth:`replace_version_in_editing_context`.
        """
        payload = body.model_dump(mode="json", by_alias=True, exclude_none=True)
        await self._request(
            "post",
            f"/core/api/editingContexts/{editing_context_id}/update",
            json=payload,
        )
        return None
