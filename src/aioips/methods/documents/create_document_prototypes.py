"""Метод создания прототипа документа для типа объекта IPS (мутация)."""

from typing import Any

from ...core import APIManager


class CreateDocumentPrototypesMixin(APIManager):
    """Реализует ``POST /api/documents/{objectTypeId}/prototypes/create``.

    operationId ``DocumentSettings_CreateDocumentPrototypes``.
    """

    async def create_document_prototypes(
        self: "CreateDocumentPrototypesMixin",
        object_type_id: int,
        *,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Создаёт прототип документа для указанного типа объекта (МУТАЦИЯ).

        Прототип документа — файл-заготовка, на основе которой создаётся новый документ.
        Метод создаёт новый (приватный) прототип, привязанный к типу объекта
        ``objectTypeId``, и возвращает описание созданного прототипа. Это операция
        ЗАПИСИ, изменяющая серверное состояние настроек документов.

        Когда применять: при программной настройке документов типа — добавлении нового
        шаблона-прототипа. Прочитать существующие прототипы можно методами
        :meth:`document_prototypes_common` и :meth:`document_prototypes_private`; обновить
        существующий — :meth:`update_document_prototypes`.

        Обратимость: создаёт новую сущность на сервере; отдельного метода удаления
        прототипа в обёртке нет. Защищена параметром ``confirm``.

        Args:
            object_type_id: Идентификатор ТИПА объекта (path-параметр ``objectTypeId``,
                int32), для которого создаётся прототип документа. Это id типа из
                метаданных, не id объекта/версии.
            confirm: Подтверждение операции записи. Без ``True`` запрос НЕ выполняется и
                поднимается :class:`ValueError` ещё до обращения к серверу.

        Returns:
            Словарь ``DocumentPrototypeOutContract`` — описание созданного прототипа
            (как сырой JSON ответа, без преобразования в схему). Значимые поля включают
            идентификатор и имя прототипа.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                created = await ips.create_document_prototypes(1116, confirm=True)
                prototype_id = created.get("id")

        Notes:
            operationId ``DocumentSettings_CreateDocumentPrototypes``; путь
            ``POST /api/documents/{objectTypeId}/prototypes/create`` (под префиксом
            ``/api/``, не ``/core/api/``). Тело не требуется (``json={}``). Ответ —
            объект ``DocumentPrototypeOutContract``.
        """
        if confirm is not True:
            raise ValueError(
                "create_document_prototypes создаёт прототип документа; передайте confirm=True",
            )
        data = await self._request(
            "post", f"/api/documents/{object_type_id}/prototypes/create", json={}
        )
        return data if isinstance(data, dict) else {}
