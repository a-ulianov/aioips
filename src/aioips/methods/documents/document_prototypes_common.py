"""Метод получения общих прототипов документов."""

from ...core import APIManager
from ...schemas.documents import DocumentPrototype


class DocumentPrototypesCommonMixin(APIManager):
    """Реализует метод ``GET /api/documents/prototypes/common``.

    operationId ``DocumentSettings_GetGeneralDocumentPrototypes``.
    """

    async def document_prototypes_common(
        self: "DocumentPrototypesCommonMixin",
    ) -> list[DocumentPrototype]:
        """Возвращает общие (доступные всем типам) прототипы документов.

        Прототип документа — это файл-заготовка, на основе которой создаётся новый
        документ. Общие прототипы не привязаны к конкретному типу объекта и могут
        использоваться в настройках документов любого типа. Их идентификаторы
        попадают в поле ``file_prototype_ids`` схемы :class:`DocumentSettings`.

        Когда применять: чтобы показать пользователю выбор шаблона при создании
        документа, доступного для любого типа, либо чтобы расшифровать общие
        прототипы из настроек типа (см. :meth:`document_settings`). Приватные
        (привязанные к типам) прототипы — :meth:`document_prototypes_private`.
        Предусловий нет.

        Returns:
            Список прототипов по схеме :class:`DocumentPrototype`. Пустой список
            означает, что общих прототипов документов не задано.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                prototypes = await ips.document_prototypes_common()
                names = {p.prototype_id: p.prototype_name for p in prototypes}

        Notes:
            operationId ``DocumentSettings_GetGeneralDocumentPrototypes``; путь
            ``GET /api/documents/prototypes/common`` (массив
            ``DocumentPrototypeOutContract``). Путь под префиксом ``/api/``
            (не ``/core/api/``).
        """
        data = await self._request("get", "/api/documents/prototypes/common")
        return [DocumentPrototype.model_validate(item) for item in data]
