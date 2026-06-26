"""Метод удаления документа из списка открытых в редакторе документов (мутация)."""

from typing import Any

from ...core import APIManager


class DocEditorRemoveFromOpenDocumentsMixin(APIManager):
    """Реализует ``DELETE /core/api/documentEditor/openDocument/{objectGuid}/{fileBlobId}/remove``.

    operationId ``DocumentEditor_RemoveFromOpenDocuments``.
    """

    async def doc_editor_remove_from_open_documents(
        self: "DocEditorRemoveFromOpenDocumentsMixin",
        object_guid: str,
        file_blob_id: int,
        *,
        confirm: bool = False,
    ) -> bool:
        """Удаляет документ из списка открытых в редакторе документов (МУТАЦИЯ сессии).

        Убирает документ из серверного списка открытых документов редактора
        (beta-функциональность IPS), освобождая связанную сессию. Изменяет состояние
        сессии (несохранённые правки теряются), поэтому защищён ``confirm``. Мягкое
        закрытие (с указанием режима) выполняет :meth:`doc_editor_close_document`;
        сохранить перед удалением — :meth:`doc_editor_save_document`.

        Защита: без ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            object_guid: GUID ОБЪЕКТА документа (``objectGUID`` — id-пространство
                объектов, не версий). Уходит в путь ``{objectGuid}``.
            file_blob_id: Идентификатор BLOB файла документа (``fileBlobId``). Уходит в
                путь ``{fileBlobId}``.
            confirm: Подтверждение мутации сессии. Без ``True`` запрос не выполняется.

        Returns:
            ``True``, если документ удалён из списка открытых; ``False`` — если сервер
            вернул отрицательный или пустой ответ.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ok = await ips.doc_editor_remove_from_open_documents(
                    "11111111-1111-1111-1111-111111111111", 42, confirm=True,
                )

        Notes:
            operationId ``DocumentEditor_RemoveFromOpenDocuments``; путь ``DELETE /core/
            api/documentEditor/openDocument/{objectGuid}/{fileBlobId}/remove`` (ответ —
            boolean). Beta-функциональность редактора документов.
        """
        if confirm is not True:
            raise ValueError(
                "doc_editor_remove_from_open_documents удаляет документ из списка "
                "открытых на сервере; передайте confirm=True",
            )
        path = f"/core/api/documentEditor/openDocument/{object_guid}/{file_blob_id}/remove"
        data: Any = await self._request("delete", path)
        return bool(data) if data is not None else False
