"""Метод проверки возможности добавить тип объекта в контекст редактирования по GUID."""

from urllib.parse import quote

from ...core import APIManager


class CanAddObjectTypeToEditingContextByGuidMixin(APIManager):
    """Реализует ``GET .../editingContext/canAddObjectType/byGuid/{objectTypeGuid}``."""

    async def can_add_object_type_to_editing_context_by_guid(
        self: "CanAddObjectTypeToEditingContextByGuidMixin",
        object_type_guid: str,
    ) -> bool:
        """Проверяет, можно ли добавить тип объекта в контекст редактирования (по GUID).

        Контекст редактирования — набор типов объектов, правящихся совместно. Не всякий тип
        допустимо включить в такой контекст; метод отвечает, разрешено ли добавление типа
        объекта с данным ``guid`` в контекст редактирования. GUID типа объекта стабилен
        между установками IPS (в отличие от ``id``). Ответ сервера — голое булево значение,
        без обёртки ``...NullableResultDto``.

        Когда применять: переносимая (по стабильному GUID) валидация на этапе настройки
        метаданных — перед включением типа в совместное редактирование. Аналог по id —
        :meth:`can_add_object_type_to_editing_context`.

        Args:
            object_type_guid: GUID типа объекта (стабильный идентификатор типа), строка
                вида ``"11111111-2222-3333-4444-555555555555"``. Кодируется в URL.

        Returns:
            ``True`` — тип объекта можно добавить в контекст редактирования; ``False`` —
            нельзя (в том числе если сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = "11111111-2222-3333-4444-555555555555"
                flag = await ips.can_add_object_type_to_editing_context_by_guid(guid)

        Notes:
            operationId ``Metadata_CanAddObjectTypeToEditingContextByGuid``; путь
            ``GET /core/api/metadata/editingContext/canAddObjectType/byGuid/{objectTypeGuid}``
            (ответ — ``boolean``). Связанный метод:
            :meth:`can_add_object_type_to_editing_context`.
        """
        encoded_guid = quote(object_type_guid, safe="")
        path = f"/core/api/metadata/editingContext/canAddObjectType/byGuid/{encoded_guid}"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
