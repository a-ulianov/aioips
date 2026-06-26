"""Метод получения дочерних узлов страницы документа в редакторе документов."""

from typing import Any

from ...core import APIManager


class DocEditorPageChildNodesMixin(APIManager):
    """Реализует ``POST /core/api/documentEditor/content/pageChildNodes``.

    operationId ``DocumentEditor_GetPageChildNodes``.
    """

    async def doc_editor_page_child_nodes(
        self: "DocEditorPageChildNodesMixin",
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Возвращает содержимое страницы документа с её дочерними узлами.

        Отдаёт модель содержимого страницы (``DocTreeNodeContentViewModel``): саму
        страницу, её dpi, порядок страниц и имена страниц. Применяется при отрисовке и
        навигации по странице документа в редакторе (beta-функциональность IPS).

        POST-verb, но операция ЧТЕНИЯ: тело несёт идентификацию страницы/контекст и
        ничего не мутирует (идемпотентно). Графическое (SVG) представление той же
        страницы отдаёт :meth:`doc_editor_page_svg`.

        Args:
            body: Тело запроса (идентификация страницы и контекст документа). Передаётся
                как есть. ``None`` — пустое тело ``{}``. Структура зависит от документа,
                поэтому принимается как ``dict[str, Any]``.

        Returns:
            Словарь ``DocTreeNodeContentViewModel`` «как есть» со значимыми ключами:
            ``page`` (узел страницы с дочерними элементами), ``dpi`` (разрешение),
            ``pagesOrderId`` (идентификатор порядка страниц), ``pageNames`` (имена
            страниц). Пустой словарь — сервер вернул пустой ответ.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                content = await ips.doc_editor_page_child_nodes({"pageId": 1})
                print(content.get("dpi"))

        Notes:
            operationId ``DocumentEditor_GetPageChildNodes``; путь
            ``POST /core/api/documentEditor/content/pageChildNodes`` (ответ —
            ``DocTreeNodeContentViewModel``). Beta-функциональность редактора документов.
        """
        data: Any = await self._request(
            "post", "/core/api/documentEditor/content/pageChildNodes", json=body or {}
        )
        return data if isinstance(data, dict) else {}
