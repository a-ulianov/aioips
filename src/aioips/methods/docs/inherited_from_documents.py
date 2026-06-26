"""Метод проверки наследования типа документа от документов (чтение через POST)."""

from typing import Any

from ...core import APIManager


class InheritedFromDocumentsMixin(APIManager):
    """Реализует ``POST /core/api/docs/InheritedFromDocuments``.

    operationId ``Documents_InheritedFromDocuments``.
    """

    async def inherited_from_documents(
        self: "InheritedFromDocumentsMixin",
        document_type: int | None = None,
    ) -> bool:
        """Сообщает, наследует ли тип документа от базового типа ДОКУМЕНТОВ (чтение).

        Проверяет, входит ли заданный тип объекта в иерархию документов (т. е.
        является ли он типом документа). Несмотря на HTTP-метод POST, это
        операция ЧТЕНИЯ — сервер ничего не изменяет, тело запроса пустое
        (``{}``), а тип передаётся query-параметром ``documentType``.

        Когда применять: чтобы отличить тип-документ от прочих типов объектов
        (например, перед обращением к методам настроек документов). Более узкая
        проверка наследования от конструкторских документов —
        :meth:`inherited_from_constructor_documents`. Предусловий нет.

        Args:
            document_type: Идентификатор ТИПА объекта (query-параметр
                ``documentType``; id типа из метаданных, не id объекта/версии).
                ``None`` — параметр не передаётся.

        Returns:
            ``True``, если тип наследует от базового типа документов, иначе
            ``False``. При не-булевом ответе сервера значение приводится к
            ``bool``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                is_doc = await ips.inherited_from_documents(1742)

        Notes:
            operationId ``Documents_InheritedFromDocuments``; путь
            ``POST /core/api/docs/InheritedFromDocuments``. Ключ query —
            ``documentType``. Тело не передаётся (``{}`` против 415). По swagger
            ответ — boolean. См. объектной модели IPS.
        """
        params: dict[str, Any] = {}
        if document_type is not None:
            params["documentType"] = document_type
        data = await self._request(
            "post", "/core/api/docs/InheritedFromDocuments", params=params, json={}
        )
        return bool(data)
