"""Метод получения содержимого документа по blob-файлу в редакторе документов."""

from typing import Any

from ...common.enumerations import OpenDocumentMode
from ...core import APIManager


class DocEditorContentMixin(APIManager):
    """Реализует ``GET /core/api/documentEditor/{objectGuid}/content/{fileBlobId}``.

    operationId ``DocumentEditor_GetDocumentContent``.
    """

    async def doc_editor_content(
        self: "DocEditorContentMixin",
        object_guid: str,
        file_blob_id: int,
        *,
        mode: OpenDocumentMode | str | None = None,
    ) -> dict[str, Any]:
        """Возвращает содержимое документа (``DocumentContentDto``) в редакторе.

        Отдаёт разобранную модель содержимого документа для конкретного
        blob-файла, привязанного к объекту. Применяйте при открытии/предпросмотре
        документа в редакторе (beta-функциональность IPS). Операция ЧТЕНИЯ,
        идемпотентна.

        Идентификация двухуровневая: ``object_guid`` — GUID ОБЪЕКТА документа (не
        версии), ``file_blob_id`` — идентификатор конкретного файла-blob внутри
        документа. Формулы того же документа отдаёт :meth:`doc_editor_formulas`.

        Args:
            object_guid: GUID объекта документа (подставляется в путь как
                ``{objectGuid}``).
            file_blob_id: Идентификатор файла-blob документа (целое, путь
                ``{fileBlobId}``).
            mode: Режим открытия документа (query ``mode``,
                ``OpenDocumentMode``). Допустимые значения: ``none``, ``edit``,
                ``view``, ``viewInCard``, ``print``, ``pdf``. ``None`` —
                параметр не передаётся. Внимание: в swagger ``mode`` помечен как
                обязательный — при пустом значении сервер может вернуть ошибку.

        Returns:
            Словарь ``DocumentContentDto`` «как есть» (структурное содержимое
            документа). Пустой словарь — сервер вернул пустой ответ.

        Raises:
            IPSNotFoundError: Если документ/blob по указанным идентификаторам нет.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                content = await ips.doc_editor_content(
                    "cad001c5-306c-11d8-b4e9-00304f19f545", 42, mode="view",
                )

        Notes:
            operationId ``DocumentEditor_GetDocumentContent``; путь
            ``GET /core/api/documentEditor/{objectGuid}/content/{fileBlobId}``;
            query ``mode`` (enum ``OpenDocumentMode``). Ответ —
            ``DocumentContentDto``. Связанный метод: :meth:`doc_editor_formulas`.
        """
        params: dict[str, Any] = {}
        if mode is not None:
            params["mode"] = mode
        data: Any = await self._request(
            "get",
            f"/core/api/documentEditor/{object_guid}/content/{file_blob_id}",
            params=params,
        )
        return data if isinstance(data, dict) else {}
