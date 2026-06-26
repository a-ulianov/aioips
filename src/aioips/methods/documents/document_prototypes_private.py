"""Метод получения приватных прототипов документов."""

from ...core import APIManager
from ...schemas.documents import DocumentPrototype


class DocumentPrototypesPrivateMixin(APIManager):
    """Реализует метод ``GET /api/documents/prototypes/private``.

    operationId ``DocumentSettings_GetPrivateDocumentPrototypes``.
    """

    async def document_prototypes_private(
        self: "DocumentPrototypesPrivateMixin",
    ) -> list[DocumentPrototype]:
        """Возвращает приватные (привязанные к типам) прототипы документов.

        Прототип документа — это файл-заготовка, на основе которой создаётся новый
        документ. Приватные прототипы, в отличие от общих, заданы для конкретных
        типов объектов и применяются только в их настройках документов. Их
        идентификаторы попадают в поле ``file_prototype_ids`` схемы
        :class:`DocumentSettings`.

        Когда применять: чтобы перечислить специфичные для типов шаблоны
        документов либо расшифровать приватные прототипы из настроек типа (см.
        :meth:`document_settings`). Общие (доступные всем типам) прототипы —
        :meth:`document_prototypes_common`. Предусловий нет.

        Returns:
            Список прототипов по схеме :class:`DocumentPrototype`. Пустой список
            означает, что приватных прототипов документов не задано.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                prototypes = await ips.document_prototypes_private()
                for proto in prototypes:
                    print(proto.prototype_id, proto.prototype_file_name)

        Notes:
            operationId ``DocumentSettings_GetPrivateDocumentPrototypes``; путь
            ``GET /api/documents/prototypes/private`` (массив
            ``DocumentPrototypeOutContract``). Путь под префиксом ``/api/``
            (не ``/core/api/``).
        """
        data = await self._request("get", "/api/documents/prototypes/private")
        return [DocumentPrototype.model_validate(item) for item in data]
