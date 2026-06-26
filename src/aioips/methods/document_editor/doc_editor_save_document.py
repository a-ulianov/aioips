"""Метод сохранения открытого документа в редакторе документов (мутация)."""

from typing import Any

from ...core import APIManager


class DocEditorSaveDocumentMixin(APIManager):
    """Реализует ``POST /core/api/documentEditor/openDocument/{objectGuid}/{fileBlobId}/save``.

    operationId ``DocumentEditor_SaveDocument``.
    """

    async def doc_editor_save_document(
        self: "DocEditorSaveDocumentMixin",
        object_guid: str,
        file_blob_id: int,
        *,
        is_virtual_document: bool | None = None,
        type_id: int | None = None,
        new_object_guid_after_save_virtual_document: str | None = None,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Сохраняет открытый в редакторе документ (МУТАЦИЯ сессии).

        Фиксирует текущее состояние документа, открытого в редакторе
        (beta-функциональность IPS), записывая изменения на сервер. Изменяет данные
        документа, поэтому защищён ``confirm``. Применяется после внесения правок (в т.ч.
        пакетом через :meth:`doc_editor_execute_batch_transactions`) перед закрытием
        сессии (:meth:`doc_editor_close_document`).

        Защита: без ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            object_guid: GUID ОБЪЕКТА документа (``objectGUID`` — id-пространство
                объектов, не версий). Уходит в путь ``{objectGuid}``.
            file_blob_id: Идентификатор BLOB файла документа (``fileBlobId``). Уходит в
                путь ``{fileBlobId}``.
            is_virtual_document: Признак сохранения как виртуального документа (query
                ``isVirtualDocument``). ``None`` — параметр не передаётся.
            type_id: Идентификатор ТИПА объекта для создаваемого документа (query
                ``typeId``, id-пространство ТИПОВ). ``None`` — параметр не передаётся.
            new_object_guid_after_save_virtual_document: GUID нового объекта после
                сохранения виртуального документа (query
                ``newObjectGuidAfterSaveVirtualDocument``). ``None`` — не передаётся.
            confirm: Подтверждение мутации. Без ``True`` запрос не выполняется.

        Returns:
            Словарь ``SaveDocumentViewModel`` «как есть» со значимыми ключами:
            ``modified`` (флаг изменения), ``modifyDate`` (дата изменения),
            ``objectGuid`` / ``objectId`` (идентификаторы объекта), ``objectTypeGuid``,
            ``fileBlobId``, ``caption``. Пустой словарь — сервер вернул пустой ответ.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                result = await ips.doc_editor_save_document(
                    "11111111-1111-1111-1111-111111111111", 42, confirm=True,
                )
                print(result.get("objectId"))

        Notes:
            operationId ``DocumentEditor_SaveDocument``; путь ``POST /core/api/
            documentEditor/openDocument/{objectGuid}/{fileBlobId}/save`` (тело — ``{}``;
            опциональные query ``isVirtualDocument`` / ``typeId`` /
            ``newObjectGuidAfterSaveVirtualDocument``; ответ — ``SaveDocumentViewModel``).
            Beta-функциональность редактора документов.
        """
        if confirm is not True:
            raise ValueError(
                "doc_editor_save_document сохраняет документ на сервере; передайте confirm=True",
            )
        path = f"/core/api/documentEditor/openDocument/{object_guid}/{file_blob_id}/save"
        params: dict[str, Any] = {}
        if is_virtual_document is not None:
            params["isVirtualDocument"] = str(is_virtual_document).lower()
        if type_id is not None:
            params["typeId"] = type_id
        if new_object_guid_after_save_virtual_document is not None:
            params["newObjectGuidAfterSaveVirtualDocument"] = (
                new_object_guid_after_save_virtual_document
            )
        data: Any = await self._request("post", path, json={}, params=params)
        return data if isinstance(data, dict) else {}
