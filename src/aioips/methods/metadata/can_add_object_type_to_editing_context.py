"""Метод проверки возможности добавить тип объекта в контекст редактирования по id."""

from ...core import APIManager


class CanAddObjectTypeToEditingContextMixin(APIManager):
    """Реализует ``GET /core/api/metadata/editingContext/canAddObjectType/{objectTypeId}``."""

    async def can_add_object_type_to_editing_context(
        self: "CanAddObjectTypeToEditingContextMixin",
        object_type_id: int,
    ) -> bool:
        """Проверяет, можно ли добавить тип объекта в контекст редактирования (по id).

        Контекст редактирования — набор типов объектов, правящихся совместно. Не всякий тип
        допустимо включить в такой контекст; метод отвечает, разрешено ли добавление типа
        объекта с данным ``id`` в контекст редактирования (например, при конфигурировании
        метаданных). Ответ сервера — голое булево значение, без обёртки
        ``...NullableResultDto``.

        Когда применять: на этапе настройки/валидации метаданных — перед попыткой включить
        тип в совместное редактирование, чтобы заранее отсечь недопустимые типы. Аналог по
        GUID — :meth:`can_add_object_type_to_editing_context_by_guid`.

        Args:
            object_type_id: Идентификатор типа объекта (id-пространство ТИПОВ объектов
                метаданных, не id объекта и не id версии).

        Returns:
            ``True`` — тип объекта можно добавить в контекст редактирования; ``False`` —
            нельзя (в том числе если сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.can_add_object_type_to_editing_context(42):
                    print("тип допустим к добавлению")

        Notes:
            operationId ``Metadata_CanAddObjectTypeToEditingContextById``; путь
            ``GET /core/api/metadata/editingContext/canAddObjectType/{objectTypeId}``
            (ответ — ``boolean``). Связанный метод:
            :meth:`can_add_object_type_to_editing_context_by_guid`.
        """
        path = f"/core/api/metadata/editingContext/canAddObjectType/{object_type_id}"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
