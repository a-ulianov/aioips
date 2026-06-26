"""Метод проверки наличия списка шрифтов редактора документов."""

from ...core import APIManager


class DocEditorFontListMixin(APIManager):
    """Реализует ``GET /core/api/documentEditor/font/getFontList``.

    operationId ``DocumentEditor_GetFontList``.
    """

    async def doc_editor_font_list(self: "DocEditorFontListMixin") -> bool:
        """Возвращает признак готовности (наличия) списка шрифтов редактора документов.

        Отдаёт булев флаг, сообщающий, доступен ли серверу список шрифтов редактора
        документов. Применяется как лёгкая проверка перед запросом имён шрифтов через
        :meth:`doc_editor_all_fonts_name`. Метод только читает.

        Когда применять: чтобы убедиться, что подсистема шрифтов редактора
        инициализирована, до обращения за полным перечнем шрифтов.

        Returns:
            ``True``, если список шрифтов доступен; ``False`` — если недоступен либо
            сервер вернул пустой ответ.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.doc_editor_font_list():
                    fonts = await ips.doc_editor_all_fonts_name()

        Notes:
            operationId ``DocumentEditor_GetFontList``; путь
            ``GET /core/api/documentEditor/font/getFontList`` (boolean).
        """
        data = await self._request("get", "/core/api/documentEditor/font/getFontList")
        return bool(data) if data is not None else False
