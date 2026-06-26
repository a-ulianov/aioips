"""Метод проверки, является ли тип объекта контекстом редактирования по GUID."""

from urllib.parse import quote

from ...core import APIManager


class IsEditingContextByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/editingContext/byGuid/{guid}/exists``."""

    async def is_editing_context_by_guid(
        self: "IsEditingContextByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, образует ли тип объекта контекст редактирования (по GUID).

        Контекст редактирования — набор типов объектов, правящихся совместно. Метод
        отвечает, является ли тип объекта с данным ``guid`` контекстом редактирования, то
        есть запускает ли его checkout совместную правку связанных типов. GUID типа объекта
        стабилен между установками IPS (в отличие от ``id``). Ответ сервера — голое булево
        значение, без обёртки ``...NullableResultDto``.

        Когда применять: переносимая (по стабильному GUID) проверка перед правкой — потянет
        ли checkout объекта этого типа подчинённые объекты в общую транзакцию. Аналог по id —
        :meth:`is_editing_context`.

        Args:
            guid: GUID типа объекта (стабильный идентификатор типа), строка вида
                ``"11111111-2222-3333-4444-555555555555"``. Кодируется в URL.

        Returns:
            ``True`` — тип объекта образует контекст редактирования; ``False`` — нет
            (в том числе если сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = "11111111-2222-3333-4444-555555555555"
                flag = await ips.is_editing_context_by_guid(guid)

        Notes:
            operationId ``Metadata_IsObjectTypeEditingContextByGuid``; путь
            ``GET /core/api/metadata/editingContext/byGuid/{guid}/exists`` (ответ —
            ``boolean``). Связанный метод: :meth:`is_editing_context`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/editingContext/byGuid/{encoded_guid}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
