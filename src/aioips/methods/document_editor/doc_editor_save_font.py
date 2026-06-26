"""Метод сохранения шрифта в редакторе документов (мутация)."""

from typing import Any

from ...core import APIManager


class DocEditorSaveFontMixin(APIManager):
    """Реализует ``POST /core/api/documentEditor/font/saveFont``.

    operationId ``DocumentEditor_SaveFont``.
    """

    async def doc_editor_save_font(
        self: "DocEditorSaveFontMixin",
        body: dict[str, Any] | None = None,
        *,
        confirm: bool = False,
    ) -> bool:
        """Сохраняет (регистрирует) шрифт в подсистеме редактора документов (МУТАЦИЯ).

        Добавляет/обновляет шрифт, доступный редактору документов (beta-функциональность
        IPS), на основании данных тела запроса. Изменяет состояние сервера (список
        шрифтов), поэтому защищён ``confirm``. Проверить наличие списка шрифтов можно
        через :meth:`doc_editor_font_list`, а перечень имён — через
        :meth:`doc_editor_all_fonts_name`.

        Защита: без ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            body: Тело запроса с данными шрифта (имя, бинарные данные/метаданные).
                Передаётся как есть. ``None`` — пустое тело ``{}``. Структура зависит от
                формата шрифта, поэтому принимается как ``dict[str, Any]``.
            confirm: Подтверждение мутации. Без ``True`` запрос не выполняется.

        Returns:
            ``True``, если шрифт сохранён; ``False`` — если сервер вернул отрицательный
            или пустой ответ.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ok = await ips.doc_editor_save_font(
                    {"name": "MyFont", "data": "..."}, confirm=True,
                )

        Notes:
            operationId ``DocumentEditor_SaveFont``; путь
            ``POST /core/api/documentEditor/font/saveFont`` (ответ — boolean).
            Beta-функциональность редактора документов.
        """
        if confirm is not True:
            raise ValueError(
                "doc_editor_save_font сохраняет шрифт на сервере; передайте confirm=True",
            )
        data: Any = await self._request(
            "post", "/core/api/documentEditor/font/saveFont", json=body or {}
        )
        return bool(data) if data is not None else False
