"""Метод получения формул документа по blob-файлу в редакторе документов."""

from typing import Any

from ...common.enumerations import OpenDocumentMode
from ...core import APIManager


class DocEditorFormulasMixin(APIManager):
    """Реализует ``GET /core/api/documentEditor/{objectGuid}/formulas/{fileBlobId}``.

    operationId ``DocumentEditor_GetFormulas``.
    """

    async def doc_editor_formulas(
        self: "DocEditorFormulasMixin",
        object_guid: str,
        file_blob_id: int,
        *,
        mode: OpenDocumentMode | str | None = None,
    ) -> list[dict[str, Any]]:
        """Возвращает список формул документа (``FormulaInfo``) в редакторе.

        Отдаёт формулы, относящиеся к конкретному blob-файлу документа.
        Применяйте при открытии/предпросмотре документа в редакторе, когда нужны
        его формулы (beta-функциональность IPS). Операция ЧТЕНИЯ, идемпотентна.
        Содержимое того же документа отдаёт :meth:`doc_editor_content`.

        Идентификация двухуровневая: ``object_guid`` — GUID ОБЪЕКТА документа (не
        версии), ``file_blob_id`` — идентификатор конкретного файла-blob.

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
            Список словарей ``FormulaInfo`` «как есть». Пустой список — формул нет
            либо сервер вернул пустой ответ.

        Raises:
            IPSNotFoundError: Если документ/blob по указанным идентификаторам нет.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                formulas = await ips.doc_editor_formulas(
                    "cad001c5-306c-11d8-b4e9-00304f19f545", 42, mode="view",
                )
                for f in formulas:
                    print(f.get("name"))

        Notes:
            operationId ``DocumentEditor_GetFormulas``; путь
            ``GET /core/api/documentEditor/{objectGuid}/formulas/{fileBlobId}``;
            query ``mode`` (enum ``OpenDocumentMode``). Расхождение с контрактом
            задачи: schema ответа в swagger — МАССИВ ``FormulaInfo``, поэтому
            метод возвращает ``list[dict]`` (не ``dict``). Связанный метод:
            :meth:`doc_editor_content`.
        """
        params: dict[str, Any] = {}
        if mode is not None:
            params["mode"] = mode
        data: Any = await self._request(
            "get",
            f"/core/api/documentEditor/{object_guid}/formulas/{file_blob_id}",
            params=params,
        )
        if not isinstance(data, list):
            return []
        return [item for item in data if isinstance(item, dict)]
