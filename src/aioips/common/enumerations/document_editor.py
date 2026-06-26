"""Перечисления раздела редактора документов IPS Web API."""

from enum import StrEnum


class OpenDocumentMode(StrEnum):
    """Режим открытия документа в редакторе (``OpenDocumentMode``).

    Используется в методах редактора документов (``mode``-параметр):
    :meth:`~aioips.IPSClient.doc_editor_close_document`,
    :meth:`~aioips.IPSClient.doc_editor_content`,
    :meth:`~aioips.IPSClient.doc_editor_formulas`.

    Attributes:
        NONE: Не задан (``none``).
        EDIT: Редактирование (``edit``).
        VIEW: Просмотр (``view``).
        VIEW_IN_CARD: Просмотр в карточке (``viewInCard``).
        PRINT: Печать (``print``).
        PDF: Экспорт/просмотр PDF (``pdf``).
    """

    NONE = "none"
    EDIT = "edit"
    VIEW = "view"
    VIEW_IN_CARD = "viewInCard"
    PRINT = "print"
    PDF = "pdf"
