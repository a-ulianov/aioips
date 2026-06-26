"""Метод получения SVG-представления страницы документа в редакторе документов."""

from typing import Any

from ...core import APIManager


class DocEditorPageSvgMixin(APIManager):
    """Реализует ``POST /core/api/documentEditor/content/pageSvg``.

    operationId ``DocumentEditor_GetPageSvg``.
    """

    async def doc_editor_page_svg(
        self: "DocEditorPageSvgMixin",
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Возвращает SVG-представление страницы документа в редакторе.

        Отдаёт модель содержимого страницы (``DocTreeNodeContentViewModel``) с её
        графическим (SVG) представлением для отрисовки в редакторе документов
        (beta-функциональность IPS). Применяется при предпросмотре/рендеринге страницы.

        POST-verb, но операция ЧТЕНИЯ: тело несёт идентификацию страницы/контекст и
        ничего не мутирует (идемпотентно). Структурную (не графическую) модель той же
        страницы отдаёт :meth:`doc_editor_page_child_nodes`.

        Args:
            body: Тело запроса (идентификация страницы и контекст документа). Передаётся
                как есть. ``None`` — пустое тело ``{}``. Структура зависит от документа,
                поэтому принимается как ``dict[str, Any]``.

        Returns:
            Словарь ``DocTreeNodeContentViewModel`` «как есть» (включает узел ``page`` с
            SVG-данными, ``dpi``, ``pagesOrderId``, ``pageNames``). Пустой словарь —
            сервер вернул пустой ответ.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                svg_model = await ips.doc_editor_page_svg({"pageId": 1})
                print(svg_model.get("page"))

        Notes:
            operationId ``DocumentEditor_GetPageSvg``; путь
            ``POST /core/api/documentEditor/content/pageSvg`` (ответ —
            ``DocTreeNodeContentViewModel``). Beta-функциональность редактора документов.
        """
        data: Any = await self._request(
            "post", "/core/api/documentEditor/content/pageSvg", json=body or {}
        )
        return data if isinstance(data, dict) else {}
