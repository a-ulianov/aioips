"""Метод предпросмотра настройки текстового модального окна редактора документов."""

from typing import Any

from ...core import APIManager


class DocEditorTextModalSettingPreviewMixin(APIManager):
    """Реализует ``POST /core/api/documentEditor/preview``.

    operationId ``DocumentEditor_GetTextModalSettingPreview``.
    """

    async def doc_editor_text_modal_setting_preview(
        self: "DocEditorTextModalSettingPreviewMixin",
        body: dict[str, Any] | None = None,
    ) -> str:
        """Возвращает предпросмотр текста по настройкам модального окна редактора.

        По переданным настройкам текстового модального окна редактора документов
        отдаёт готовую строку предпросмотра (как текст будет выглядеть с учётом формата,
        подстановок и оформления). Применяется для интерактивного предпросмотра при
        настройке текстовых элементов (beta-функциональность IPS).

        POST-verb, но операция ЧТЕНИЯ: формирует предпросмотр по входным настройкам и
        ничего не мутирует на сервере (идемпотентно).

        Args:
            body: Тело запроса с настройками текстового модального окна. Передаётся как
                есть. ``None`` — пустое тело ``{}``. Структура настроек полиморфна,
                поэтому принимается как ``dict[str, Any]``.

        Returns:
            Строка предпросмотра текста. Если сервер вернул пустой ответ (``None``),
            возвращается пустая строка ``""``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                text = await ips.doc_editor_text_modal_setting_preview(
                    {"template": "{name}", "values": {"name": "Узел"}},
                )
                print(text)

        Notes:
            operationId ``DocumentEditor_GetTextModalSettingPreview``; путь
            ``POST /core/api/documentEditor/preview`` (ответ — string).
            Beta-функциональность редактора документов.
        """
        data: Any = await self._request("post", "/core/api/documentEditor/preview", json=body or {})
        return str(data) if data is not None else ""
