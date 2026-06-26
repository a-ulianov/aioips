"""Метод получения текущего шрифта в редакторе документов."""

from typing import Any

from ...core import APIManager


class DocEditorGetFontMixin(APIManager):
    """Реализует ``GET /core/api/documentEditor/font/getFont``.

    operationId ``DocumentEditor_GetFont``.
    """

    async def doc_editor_get_font(self: "DocEditorGetFontMixin") -> dict[str, Any]:
        """Возвращает сведения о текущем шрифте редактора документов.

        Справочное чтение раздела редактора документов (beta-функциональность
        IPS): запрашивает информацию о шрифте без параметров. Применяйте при
        инициализации/синхронизации настроек шрифта в редакторе. Операция ЧТЕНИЯ,
        идемпотентна, query-параметров нет.

        Args:
            None.

        Returns:
            Словарь-описание шрифта «как есть». Пустой словарь — сервер вернул
            пустой ответ или скалярный ответ (см. Notes).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                font = await ips.doc_editor_get_font()

        Notes:
            operationId ``DocumentEditor_GetFont``; путь
            ``GET /core/api/documentEditor/font/getFont`` (без query). Расхождение
            со swagger: схема ответа объявлена как ``boolean`` — на реальном
            сервере форма ответа требует проверки на проде; при скалярном ответе
            метод возвращает ``{}``. Связанные методы:
            :meth:`doc_editor_save_font`, :meth:`doc_editor_all_fonts_name`.
        """
        data: Any = await self._request(
            "get",
            "/core/api/documentEditor/font/getFont",
        )
        return data if isinstance(data, dict) else {}
