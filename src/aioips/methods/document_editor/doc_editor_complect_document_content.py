"""Метод получения содержимого комплектного документа в редакторе документов."""

from typing import Any

from ...core import APIManager


class DocEditorComplectDocumentContentMixin(APIManager):
    """Реализует ``GET /core/api/documentEditor/{objectGuid}/complectDocumentContent``.

    operationId ``DocumentEditor_GetComplectDocumentContent``.
    """

    async def doc_editor_complect_document_content(
        self: "DocEditorComplectDocumentContentMixin",
        object_guid: str,
    ) -> dict[str, Any]:
        """Возвращает содержимое комплектного (сборного) документа в редакторе.

        Отдаёт модель содержимого документа-комплекта (объединяющего несколько
        документов) для объекта. Применяйте при открытии/предпросмотре
        комплектного документа в редакторе (beta-функциональность IPS). Операция
        ЧТЕНИЯ, идемпотентна. В отличие от :meth:`doc_editor_content`, не требует
        идентификатора конкретного blob-файла.

        Идентификация: ``object_guid`` — GUID ОБЪЕКТА документа (не версии).

        Args:
            object_guid: GUID объекта комплектного документа (подставляется в
                путь как ``{objectGuid}``).

        Returns:
            Словарь содержимого комплектного документа «как есть». Пустой словарь —
            сервер вернул пустой ответ.

        Raises:
            IPSNotFoundError: Если документ по указанному GUID не найден.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                content = await ips.doc_editor_complect_document_content(
                    "cad001c5-306c-11d8-b4e9-00304f19f545",
                )

        Notes:
            operationId ``DocumentEditor_GetComplectDocumentContent``; путь
            ``GET /core/api/documentEditor/{objectGuid}/complectDocumentContent``.
            Связанный метод: :meth:`doc_editor_content`.
        """
        data: Any = await self._request(
            "get",
            f"/core/api/documentEditor/{object_guid}/complectDocumentContent",
        )
        return data if isinstance(data, dict) else {}
