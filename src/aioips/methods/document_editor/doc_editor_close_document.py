"""Метод закрытия открытого документа в редакторе документов (мутация сессии)."""

from typing import Any

from ...common.enumerations import OpenDocumentMode
from ...core import APIManager


class DocEditorCloseDocumentMixin(APIManager):
    """Реализует ``POST /core/api/documentEditor/openDocument/{objectGuid}/{fileBlobId}/close``.

    operationId ``DocumentEditor_CloseDocument``.
    """

    async def doc_editor_close_document(
        self: "DocEditorCloseDocumentMixin",
        object_guid: str,
        file_blob_id: int,
        *,
        mode: OpenDocumentMode | str = OpenDocumentMode.EDIT,
        confirm: bool = False,
    ) -> None:
        """Закрывает открытый в редакторе документ (МУТАЦИЯ сессии).

        Завершает серверную сессию редактирования документа, открытого ранее в редакторе
        (beta-функциональность IPS). Закрытие изменяет состояние сессии (несохранённые
        правки могут быть потеряны), поэтому защищено ``confirm``. Чтобы зафиксировать
        изменения перед закрытием, используйте :meth:`doc_editor_save_document`; полностью
        убрать документ из списка открытых — :meth:`doc_editor_remove_from_open_documents`.

        Защита: без ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            object_guid: GUID ОБЪЕКТА документа (``objectGUID`` — id-пространство
                объектов, не версий). Уходит в путь ``{objectGuid}``.
            file_blob_id: Идентификатор BLOB файла документа (``fileBlobId``). Уходит в
                путь ``{fileBlobId}``.
            mode: Режим, в котором документ был открыт (``OpenDocumentMode``).
                Обязательный query-параметр ``mode``. Допустимые значения: ``"none"``,
                ``"edit"`` (по умолчанию), ``"view"``, ``"viewInCard"``, ``"print"``,
                ``"pdf"``.
            confirm: Подтверждение мутации сессии. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.doc_editor_close_document(
                    "11111111-1111-1111-1111-111111111111", 42,
                    mode="edit", confirm=True,
                )

        Notes:
            operationId ``DocumentEditor_CloseDocument``; путь ``POST /core/api/
            documentEditor/openDocument/{objectGuid}/{fileBlobId}/close`` (тело — ``{}``;
            обязательный query ``mode``). Beta-функциональность редактора документов.
        """
        if confirm is not True:
            raise ValueError(
                "doc_editor_close_document закрывает сессию документа на сервере; "
                "передайте confirm=True",
            )
        path = f"/core/api/documentEditor/openDocument/{object_guid}/{file_blob_id}/close"
        params: dict[str, Any] = {"mode": mode}
        await self._request("post", path, json={}, params=params)
        return None
