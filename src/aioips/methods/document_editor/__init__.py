"""Методы раздела редактора документов IPS Web API (справочные чтения)."""

from .doc_editor_all_fonts_name import DocEditorAllFontsNameMixin
from .doc_editor_buffer import DocEditorBufferMixin
from .doc_editor_close_document import DocEditorCloseDocumentMixin
from .doc_editor_complect_document_content import DocEditorComplectDocumentContentMixin
from .doc_editor_content import DocEditorContentMixin
from .doc_editor_element_props import DocEditorElementPropsMixin
from .doc_editor_execute_batch_transactions import DocEditorExecuteBatchTransactionsMixin
from .doc_editor_font_list import DocEditorFontListMixin
from .doc_editor_formulas import DocEditorFormulasMixin
from .doc_editor_general_formulas_view import DocEditorGeneralFormulasViewMixin
from .doc_editor_get_font import DocEditorGetFontMixin
from .doc_editor_non_assignable_prop_name import DocEditorNonAssignablePropNameMixin
from .doc_editor_page_child_nodes import DocEditorPageChildNodesMixin
from .doc_editor_page_svg import DocEditorPageSvgMixin
from .doc_editor_prop_name import DocEditorPropNameMixin
from .doc_editor_remove_from_open_documents import DocEditorRemoveFromOpenDocumentsMixin
from .doc_editor_save_document import DocEditorSaveDocumentMixin
from .doc_editor_save_font import DocEditorSaveFontMixin
from .doc_editor_text_modal_setting_preview import DocEditorTextModalSettingPreviewMixin


class DocumentEditorAPI(
    DocEditorBufferMixin,
    DocEditorPropNameMixin,
    DocEditorNonAssignablePropNameMixin,
    DocEditorAllFontsNameMixin,
    DocEditorFontListMixin,
    # чтения содержимого/предпросмотра
    DocEditorElementPropsMixin,
    DocEditorPageChildNodesMixin,
    DocEditorPageSvgMixin,
    DocEditorGeneralFormulasViewMixin,
    DocEditorTextModalSettingPreviewMixin,
    # мутации сессии документа (confirm)
    DocEditorSaveFontMixin,
    DocEditorExecuteBatchTransactionsMixin,
    DocEditorCloseDocumentMixin,
    DocEditorRemoveFromOpenDocumentsMixin,
    DocEditorSaveDocumentMixin,
    DocEditorComplectDocumentContentMixin,
    DocEditorContentMixin,
    DocEditorFormulasMixin,
    DocEditorGetFontMixin,
):
    """Объединяет справочные методы чтения раздела редактора документов.

    References:
        Эндпоинты ``/core/api/documentEditor/*`` IPS Server Web API.
    """


__all__ = ["DocumentEditorAPI"]
