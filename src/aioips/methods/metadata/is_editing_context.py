"""Метод проверки, является ли тип объекта контекстом редактирования по id."""

from ...core import APIManager


class IsEditingContextMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/editingContext/{id}/exists``."""

    async def is_editing_context(
        self: "IsEditingContextMixin",
        id: int,
    ) -> bool:
        """Проверяет, образует ли тип объекта контекст редактирования (по id).

        Контекст редактирования — набор типов объектов, правящихся совместно. Метод
        отвечает, является ли тип объекта с данным ``id`` контекстом редактирования, то есть
        запускает ли его checkout совместную правку связанных типов. Ответ сервера — голое
        булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: чтобы перед началом правки понять, потянет ли checkout объекта
        этого типа за собой подчинённые объекты в общую транзакцию. Аналог по GUID —
        :meth:`is_editing_context_by_guid`; упрощённость контекста —
        :meth:`is_simple_editing_context`.

        Args:
            id: Идентификатор типа объекта (id-пространство ТИПОВ объектов метаданных,
                не id объекта и не id версии).

        Returns:
            ``True`` — тип объекта образует контекст редактирования; ``False`` — нет
            (в том числе если сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.is_editing_context(42):
                    print("checkout затронет связанные типы")

        Notes:
            operationId ``Metadata_IsObjectTypeEditingContextById``; путь
            ``GET /core/api/metadata/editingContext/{id}/exists`` (ответ — ``boolean``).
            Связанные методы: :meth:`is_editing_context_by_guid`,
            :meth:`is_simple_editing_context`.
        """
        path = f"/core/api/metadata/editingContext/{id}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
