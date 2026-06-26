"""Метод добавления объектов в контекст редактирования."""

from ...core import APIManager
from ...schemas.editing_contexts import AddObjectsToContext, AddObjectsToContextResult


class AddObjectsToEditingContextMixin(APIManager):
    """Реализует ``EditingContexts_AddObjectsToEditingContext`` (добавление в контекст)."""

    async def add_objects_to_editing_context(
        self: "AddObjectsToEditingContextMixin",
        editing_context_id: int,
        body: AddObjectsToContext,
    ) -> AddObjectsToContextResult:
        """Добавляет версии объектов в контекст редактирования (МУТИРУЮЩАЯ операция).

        Контекст редактирования — это рабочий набор версий объектов, над которым
        ведётся совместная правка (групповое извлечение/сохранение). Метод добавляет
        в указанный контекст перечисленные версии объектов и, при необходимости, их
        состав (один уровень или рекурсивно — см. ``add_objects_to_context_type`` в теле).

        Когда применять: чтобы наполнить уже созданный контекст редактирования
        объектами перед групповой обработкой. Часть объектов может быть пропущена
        (например, уже состоит в контексте) — это отражается в счётчиках результата.

        Предусловия по id-пространству: ``editing_context_id`` — идентификатор самого
        контекста редактирования; ``object_version_ids`` в теле — это ``id`` ВЕРСИЙ
        объектов (F_ID), а не ``objectID`` объектов.

        Args:
            editing_context_id: Идентификатор контекста редактирования, в который
                добавляются объекты (подставляется в путь ``{editingContextId}``).
            body: Тело запроса :class:`AddObjectsToContext` — список ``id`` версий и
                способ добавления (только объекты / с составом / с рекурсивным составом).

        Returns:
            Результат :class:`AddObjectsToContextResult` со счётчиками добавленных
            (``added_objects_count``) и пропущенных (``skipped_objects_count``)
            объектов и журналом проблем по отдельным объектам.

        Raises:
            IPSForbiddenError: При отсутствии прав на изменение контекста.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            from aioips.schemas.editing_contexts import (
                AddObjectsToContext,
                AddObjectsToEditingContextType,
            )

            async with IPSClient(config=config) as ips:
                result = await ips.add_objects_to_editing_context(
                    501,
                    AddObjectsToContext(
                        object_version_ids=[102550, 102551],
                        add_objects_to_context_type=AddObjectsToEditingContextType.OBJECTS,
                    ),
                )
                print(result.added_objects_count, result.skipped_objects_count)

        Notes:
            ``operationId``: ``EditingContexts_AddObjectsToEditingContext``; путь
            ``POST /core/api/editingContexts/{editingContextId}/add``. Связанные методы:
            :meth:`replace_version_in_editing_context`, :meth:`update_editing_context_objects`.
        """
        payload = body.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post",
            f"/core/api/editingContexts/{editing_context_id}/add",
            json=payload,
        )
        result = data.get("result", data) if isinstance(data, dict) else data
        return AddObjectsToContextResult.model_validate(result)
