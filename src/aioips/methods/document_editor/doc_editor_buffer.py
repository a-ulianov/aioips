"""Метод получения структуры документа из буфера редактора документов."""

from typing import Any

from ...core import APIManager
from ...schemas.document_editor import DocTreeNode


class DocEditorBufferMixin(APIManager):
    """Реализует ``GET /core/api/documentEditor/getBuffer`` (``DocumentEditor_GetBuffer``)."""

    async def doc_editor_buffer(self: "DocEditorBufferMixin") -> list[DocTreeNode]:
        """Возвращает структуру документа из буфера редактора как дерево узлов.

        Отдаёт корневые узлы дерева структуры документа, помещённого в буфер редактора
        документов (beta-функциональность IPS). Каждый узел описывает элемент документа
        (страница, контейнер, таблица, ячейка, надпись и т.п.) и содержит список
        дочерних узлов той же схемы — то есть результат образует рекурсивное дерево.

        Когда применять: для справочного чтения и обхода структуры документа в буфере —
        например, чтобы перечислить элементы, построить навигацию по документу или
        проверить его состав. Метод только читает; бинарное содержимое элементов,
        формулы и шрифты этим методом не извлекаются.

        Returns:
            Список корневых узлов :class:`DocTreeNode`. Каждый узел несёт «сырое»
            описание элемента (``element``) и рекурсивные дочерние узлы (``childs``).
            Пустой список означает, что буфер редактора не содержит документа.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                roots = await ips.doc_editor_buffer()
                for node in roots:
                    print(len(node.childs))

        Notes:
            operationId ``DocumentEditor_GetBuffer``; путь
            ``GET /core/api/documentEditor/getBuffer`` (массив ``DocTreeNode``).
            Beta-функциональность редактора документов.
        """
        data: Any = await self._request("get", "/core/api/documentEditor/getBuffer")
        return [DocTreeNode.model_validate(item) for item in data]
