"""Метод проверки наследования типа документа от конструкторских (чтение через POST)."""

from typing import Any

from ...core import APIManager


class InheritedFromConstructorDocumentsMixin(APIManager):
    """Реализует ``POST /core/api/docs/InheritedFromConstructorDocuments``.

    operationId ``Documents_InheritedFromConstructorDocuments``.
    """

    async def inherited_from_constructor_documents(
        self: "InheritedFromConstructorDocumentsMixin",
        document_type: int | None = None,
    ) -> bool:
        """Сообщает, наследует ли тип документа от КОНСТРУКТОРСКИХ документов (чтение).

        Проверяет, входит ли заданный тип документа в иерархию конструкторских
        документов (т. е. унаследован ли он от базового конструкторского типа).
        Несмотря на HTTP-метод POST, это операция ЧТЕНИЯ — сервер ничего не
        изменяет, тело запроса пустое (``{}``), а тип документа передаётся
        query-параметром ``documentType``.

        Когда применять: чтобы понять, применимы ли к типу правила обработки
        конструкторской документации. Более общая проверка наследования от
        документов вообще — :meth:`inherited_from_documents`. Предусловий нет.

        Args:
            document_type: Идентификатор ТИПА документа (query-параметр
                ``documentType``; id типа из метаданных, не id объекта/версии).
                ``None`` — параметр не передаётся.

        Returns:
            ``True``, если тип наследует от конструкторских документов, иначе
            ``False``. При не-булевом ответе сервера значение приводится к
            ``bool``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                is_ctor = await ips.inherited_from_constructor_documents(1742)

        Notes:
            operationId ``Documents_InheritedFromConstructorDocuments``; путь
            ``POST /core/api/docs/InheritedFromConstructorDocuments``. Ключ query
            — ``documentType``. Тело не передаётся (``{}`` против 415). По
            swagger ответ — boolean. См. объектной модели IPS.
        """
        params: dict[str, Any] = {}
        if document_type is not None:
            params["documentType"] = document_type
        data = await self._request(
            "post",
            "/core/api/docs/InheritedFromConstructorDocuments",
            params=params,
            json={},
        )
        return bool(data)
