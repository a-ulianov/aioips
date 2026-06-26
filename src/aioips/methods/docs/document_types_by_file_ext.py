"""Метод получения типов документов по расширению файла (чтение через POST)."""

from typing import Any

from ...core import APIManager


class DocumentTypesByFileExtMixin(APIManager):
    """Реализует ``POST /core/api/docs/GetDocumentTypesByFileExt``.

    operationId ``Documents_GetDocumentTypesByFileExt``.
    """

    async def document_types_by_file_ext(
        self: "DocumentTypesByFileExtMixin",
        file_ext: str | None = None,
    ) -> list[Any]:
        """Возвращает типы документов, допускающие файл с заданным расширением (чтение).

        По расширению файла (``.pdf``, ``.dwg`` и т. п.) определяет, документы
        каких типов могут хранить такой файл. Несмотря на HTTP-метод POST, это
        операция ЧТЕНИЯ — сервер ничего не изменяет, тело запроса пустое
        (``{}``), а расширение передаётся query-параметром ``fileExt``.

        Когда применять: при загрузке файла — чтобы предложить пользователю
        подходящие типы документов. Связанный метод —
        :meth:`document_types_by_output_object_types` (подбор по выходным типам
        объектов). Предусловий нет.

        Args:
            file_ext: Расширение файла (передаётся как query-параметр
                ``fileExt``; формат расширения — как ожидает сервер, обычно с
                ведущей точкой, например ``".pdf"``). ``None`` — параметр не
                передаётся.

        Returns:
            Список идентификаторов типов документов. По swagger это массив целых
            (``list[int]``); элементы передаются как есть. Пустой список ``[]``,
            если подходящих типов нет или сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                type_ids = await ips.document_types_by_file_ext(".pdf")

        Notes:
            operationId ``Documents_GetDocumentTypesByFileExt``; путь
            ``POST /core/api/docs/GetDocumentTypesByFileExt``. Ключ query —
            ``fileExt``. Тело не передаётся (``{}`` против 415). По swagger
            ответ — массив int. См. объектной модели IPS.
        """
        params: dict[str, Any] = {}
        if file_ext is not None:
            params["fileExt"] = file_ext
        data = await self._request(
            "post", "/core/api/docs/GetDocumentTypesByFileExt", params=params, json={}
        )
        return list(data) if isinstance(data, list) else []
