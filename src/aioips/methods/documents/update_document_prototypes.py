"""Метод обновления прототипа документа IPS (мутация)."""

from ...core import APIManager


class UpdateDocumentPrototypesMixin(APIManager):
    """Реализует ``POST /api/documents/prototypes/{prototypeId}``.

    operationId ``DocumentSettings_UpdateDocumentPrototypes``.
    """

    async def update_document_prototypes(
        self: "UpdateDocumentPrototypesMixin",
        prototype_id: int,
        *,
        confirm: bool = False,
    ) -> None:
        """Обновляет прототип документа по его идентификатору (МУТАЦИЯ).

        Прототип документа — файл-заготовка, на основе которой создаётся новый документ.
        Метод применяет обновление к существующему прототипу, идентифицируемому путём
        (``prototypeId``). Это операция ЗАПИСИ, изменяющая серверное состояние настроек
        документов.

        Когда применять: при программном обслуживании прототипов документов (после
        изменения связанного файла/настроек прототипа). Перечислить прототипы можно
        методами :meth:`document_prototypes_common` (общие) и
        :meth:`document_prototypes_private` (приватные, привязанные к типам). Создать
        новый прототип — :meth:`create_document_prototypes`.

        Обратимость: операция изменяет состояние прототипа на сервере; отдельного метода
        отката в обёртке нет, поэтому применяется осознанно. Защищена параметром
        ``confirm``.

        Args:
            prototype_id: Идентификатор обновляемого прототипа документа (path-параметр
                ``prototypeId``; ``prototype_id`` из :class:`DocumentPrototype`).
            confirm: Подтверждение операции записи. Без ``True`` запрос НЕ выполняется и
                поднимается :class:`ValueError` ещё до обращения к серверу.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если прототип не найден).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.update_document_prototypes(1742, confirm=True)

        Notes:
            operationId ``DocumentSettings_UpdateDocumentPrototypes``; путь
            ``POST /api/documents/prototypes/{prototypeId}`` (под префиксом ``/api/``,
            не ``/core/api/``). Тело не требуется (``json={}``). Ответ — void (None).
        """
        if confirm is not True:
            raise ValueError(
                "update_document_prototypes изменяет прототип документа; передайте confirm=True",
            )
        await self._request("post", f"/api/documents/prototypes/{prototype_id}", json={})
        return None
