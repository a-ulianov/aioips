"""Метод замены версии объекта в контексте редактирования."""

from ...core import APIManager
from ...schemas.editing_contexts import ReplaceVersionInEditingContext


class ReplaceVersionInEditingContextMixin(APIManager):
    """Реализует ``EditingContexts_ReplaceVersionInEditingContext`` (замена версии)."""

    async def replace_version_in_editing_context(
        self: "ReplaceVersionInEditingContextMixin",
        editing_context_id: int,
        body: ReplaceVersionInEditingContext,
    ) -> None:
        """Заменяет версию объекта в контексте редактирования (МУТИРУЮЩАЯ операция).

        Контекст редактирования — это рабочий набор версий объектов для совместной
        правки. Метод заменяет одну версию объекта, уже состоящую в контексте, на
        другую версию того же объекта (например, при переходе на актуальную версию).

        Когда применять: когда в контексте нужно подменить конкретную версию объекта,
        не пересобирая весь контекст. Для массового приведения объектов к актуальному
        состоянию используйте :meth:`update_editing_context_objects`.

        Предусловия по id-пространству: ``editing_context_id`` — идентификатор контекста
        редактирования; ``editing_context_version_id`` и ``replacement_version_id`` в
        теле — это ``id`` ВЕРСИЙ объектов (F_ID), а не ``objectID`` объектов.

        Args:
            editing_context_id: Идентификатор контекста редактирования (подставляется
                в путь ``{editingContextId}``).
            body: Тело запроса :class:`ReplaceVersionInEditingContext` — ``id`` версии в
                контексте (``editing_context_version_id``) и ``id`` версии-замены
                (``replacement_version_id``).

        Returns:
            ``None``. Сервер не возвращает содержательного тела (void).

        Raises:
            IPSForbiddenError: При отсутствии прав на изменение контекста.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            from aioips.schemas.editing_contexts import ReplaceVersionInEditingContext

            async with IPSClient(config=config) as ips:
                await ips.replace_version_in_editing_context(
                    501,
                    ReplaceVersionInEditingContext(
                        editing_context_version_id=102550,
                        replacement_version_id=102560,
                    ),
                )

        Notes:
            ``operationId``: ``EditingContexts_ReplaceVersionInEditingContext``; путь
            ``POST /core/api/editingContexts/{editingContextId}/replace``. Связанные
            методы: :meth:`add_objects_to_editing_context`,
            :meth:`update_editing_context_objects`.
        """
        payload = body.model_dump(mode="json", by_alias=True, exclude_none=True)
        await self._request(
            "post",
            f"/core/api/editingContexts/{editing_context_id}/replace",
            json=payload,
        )
        return None
