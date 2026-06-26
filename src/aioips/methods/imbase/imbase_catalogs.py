"""Метод получения списка идентификаторов каталогов справочной системы IMBASE."""

from typing import Any

from ...core import APIManager


class ImBaseCatalogsMixin(APIManager):
    """Реализует метод ``GET /core/api/imbase/catalogs`` (``ImBase_GetCatalogIdList``)."""

    async def imbase_catalogs(self: "ImBaseCatalogsMixin") -> list[int] | None:
        """Возвращает идентификаторы каталогов справочной системы IMBASE.

        Каталог IMBASE — корневой узел справочной системы (например, набор таблиц/
        классификаторов). Метод отдаёт идентификаторы всех каталогов верхнего уровня.

        Когда применять: чтобы перечислить доступные каталоги IMBASE (например, для
        навигации). Для подбора каталогов, подходящих под конкретный тип объекта и тип
        атрибута, используйте :meth:`imbase_supported_catalogs`; для метаданных индексов —
        :meth:`imbase_indexes`. Предусловий нет (операция чтения).

        Returns:
            Список идентификаторов каталогов (``list[int]``). Возвращает ``None``, если
            сервер сообщил об отсутствии сущности (result-обёртка с ``entity = null``);
            пустой список означает, что каталогов нет, но сущность присутствует.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                catalog_ids = await ips.imbase_catalogs()
                if catalog_ids:
                    print(len(catalog_ids))

        Notes:
            operationId ``ImBase_GetCatalogIdList``; путь ``GET /core/api/imbase/catalogs``.
            Ответ — result-обёртка ``Int64IEnumerableNullableResultDto``
            (``{entity, isEntityPresent}``), разворачивается в ``list[int] | None``.
            См. объектной модели IPS.
        """
        data = await self._request("get", "/core/api/imbase/catalogs")
        entity: Any = data.get("entity") if isinstance(data, dict) else None
        return [int(item) for item in entity] if entity is not None else None
