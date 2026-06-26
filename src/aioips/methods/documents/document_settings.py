"""Метод получения настроек документов для типа объекта."""

from ...core import APIManager
from ...schemas.documents import DocumentSettings


class DocumentSettingsMixin(APIManager):
    """Реализует метод ``GET /api/documents/{objectTypeId}/settings``.

    operationId ``DocumentSettings_GetDocumentSettings``.
    """

    async def document_settings(
        self: "DocumentSettingsMixin",
        object_type_id: int,
    ) -> DocumentSettings:
        """Возвращает настройки документов для заданного типа объекта.

        Настройки документов описывают, как обрабатываются документы данного типа
        объекта: расширения файлов, имя/код типа документа, признаки оформления
        (имя в штампе, код в обозначении), типы объектов-результатов вывода,
        подписчиков-получателей копий и идентификаторы доступных прототипов файлов.

        Когда применять: чтобы прочитать конфигурацию документооборота конкретного
        типа объекта (например, перед созданием документа или для отображения его
        настроек). Прототипы из ``file_prototype_ids`` расшифровываются методами
        :meth:`document_prototypes_common` / :meth:`document_prototypes_private`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (``objectTypeId``), для
                которого запрашиваются настройки документов. Это идентификатор типа
                из метаданных, а не идентификатор объекта (``objectID``) или версии.

        Returns:
            Настройки по схеме :class:`DocumentSettings`. Объект возвращается всегда
            (для типов без явных настроек поля принимают пустые значения/дефолты).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                settings = await ips.document_settings(1024)  # 1024 = id типа объекта
                print(settings.document_type_name, settings.file_prototype_ids)

        Notes:
            operationId ``DocumentSettings_GetDocumentSettings``; путь
            ``GET /api/documents/{objectTypeId}/settings``
            (``DocumentSettingsContract``). Путь под префиксом ``/api/``
            (не ``/core/api/``).
        """
        data = await self._request("get", f"/api/documents/{object_type_id}/settings")
        return DocumentSettings.model_validate(data)
