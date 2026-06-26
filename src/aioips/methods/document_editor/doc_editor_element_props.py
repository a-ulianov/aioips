"""Метод получения свойств элемента документа в редакторе документов."""

from typing import Any

from ...core import APIManager


class DocEditorElementPropsMixin(APIManager):
    """Реализует ``POST /core/api/documentEditor/content/getElementProps``.

    operationId ``DocumentEditor_GetElementProps``.
    """

    async def doc_editor_element_props(
        self: "DocEditorElementPropsMixin",
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Возвращает свойства конкретного элемента документа в редакторе.

        Отдаёт «сырой» набор свойств одного элемента документа (страница, контейнер,
        надпись, ячейка и т.п.), идентифицируемого данными из тела запроса. Применяется
        для чтения текущих параметров элемента (геометрия, оформление, привязки) при
        работе в редакторе документов (beta-функциональность IPS).

        POST-verb, но операция ЧТЕНИЯ: тело несёт идентификацию/контекст элемента и
        ничего на сервере не мутирует (идемпотентно). Для обхода всего дерева
        используйте :meth:`doc_editor_buffer`, для дочерних узлов страницы —
        :meth:`doc_editor_page_child_nodes`.

        Args:
            body: Тело запроса (идентификация элемента и контекст страницы/документа).
                Передаётся как есть. ``None`` — пустое тело ``{}`` (поведение сервера по
                умолчанию). Структура полиморфна и зависит от типа элемента, поэтому
                принимается как ``dict[str, Any]``.

        Returns:
            Словарь свойств элемента (``object``) «как есть». Пустой словарь означает,
            что сервер вернул пустой ответ.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                props = await ips.doc_editor_element_props(
                    {"pageId": 1, "elementId": 42},
                )
                print(props.get("width"))

        Notes:
            operationId ``DocumentEditor_GetElementProps``; путь
            ``POST /core/api/documentEditor/content/getElementProps`` (тело — inline
            object; ответ — object). Beta-функциональность редактора документов.
        """
        data: Any = await self._request(
            "post", "/core/api/documentEditor/content/getElementProps", json=body or {}
        )
        return data if isinstance(data, dict) else {}
