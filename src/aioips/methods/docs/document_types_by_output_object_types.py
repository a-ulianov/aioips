"""Метод получения типов документов по выходным типам объектов (чтение через POST)."""

from typing import Any

from ...core import APIManager


class DocumentTypesByOutputObjectTypesMixin(APIManager):
    """Реализует ``POST /core/api/docs/GetDocumentTypesByOutputObjectTypes``.

    operationId ``Documents_GetDocumentTypesByOutputObjectTypes``.
    """

    async def document_types_by_output_object_types(
        self: "DocumentTypesByOutputObjectTypesMixin",
        object_type_ids: list[int],
        *,
        root_document_object_type: int | None = None,
    ) -> list[Any]:
        """Возвращает типы документов по их выходным типам объектов (чтение).

        Подбирает типы документов, для которых заданные типы объектов являются
        выходными (результатом вывода/генерации документа). Несмотря на
        HTTP-метод POST, это операция ЧТЕНИЯ — сервер ничего не изменяет;
        перечень типов объектов передаётся телом-списком, а опциональный
        корневой тип документа — query-параметром ``rootDocumentObjectType``.

        Когда применять: чтобы по типам объектов-результатов определить, какие
        типы документов их порождают. Связанный метод —
        :meth:`document_types_by_file_ext` (подбор по расширению файла).
        Предусловий нет.

        Args:
            object_type_ids: Список идентификаторов ТИПОВ объектов
                (``objectTypeId`` из метаданных, не id объекта/версии),
                рассматриваемых как выходные. Передаётся телом запроса
                (``json``-массив целых).
            root_document_object_type: Идентификатор корневого типа объекта
                документа (query-параметр ``rootDocumentObjectType``), сужающий
                выборку. ``None`` — параметр не передаётся.

        Returns:
            Список идентификаторов типов документов. По swagger это массив целых
            (``list[int]``); элементы передаются как есть. Пустой список ``[]``,
            если подходящих типов нет или сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                type_ids = await ips.document_types_by_output_object_types(
                    [1024, 1042], root_document_object_type=1001
                )

        Notes:
            operationId ``Documents_GetDocumentTypesByOutputObjectTypes``; путь
            ``POST /core/api/docs/GetDocumentTypesByOutputObjectTypes``. Тело —
            массив int (``json=object_type_ids``); ключ query —
            ``rootDocumentObjectType``. По swagger ответ — массив int.
            См. объектной модели IPS.
        """
        params: dict[str, Any] = {}
        if root_document_object_type is not None:
            params["rootDocumentObjectType"] = root_document_object_type
        data = await self._request(
            "post",
            "/core/api/docs/GetDocumentTypesByOutputObjectTypes",
            params=params,
            json=object_type_ids,
        )
        return list(data) if isinstance(data, list) else []
