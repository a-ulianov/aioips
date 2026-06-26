"""Метод получения идентификатора каталога IMBASE по id объекта."""

from ...core import APIManager


class ImBaseCatalogIdByObjectMixin(APIManager):
    """Реализует ``GET /core/api/imbase/object/{objectId}/catalog/id``."""

    async def imbase_catalog_id_by_object(
        self: "ImBaseCatalogIdByObjectMixin",
        object_id: int,
    ) -> int:
        """Возвращает идентификатор каталога IMBASE, которому принадлежит объект.

        По объекту IMBASE определяет корневой каталог (узел верхнего уровня), в дереве
        которого он расположен. Быстрая альтернатива получению полного пути
        (:meth:`imbase_object_path`), когда нужен только id каталога. Ответ — целое
        число (не объект-обёртка).

        Когда применять: чтобы узнать, к какому каталогу относится запись/папка IMBASE,
        без построения всей цепочки пути. Полный путь — :meth:`imbase_object_path`;
        список всех каталогов — :meth:`imbase_catalogs`.

        Args:
            object_id: Идентификатор объекта IMBASE (id-пространство объектов IMBASE).

        Returns:
            Идентификатор каталога IMBASE (``int``). Сервер не возвращает ``None``:
            при отсутствии объекта — ошибка.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если объект не найден).

        Example:
            async with IPSClient(config=config) as ips:
                catalog_id = await ips.imbase_catalog_id_by_object(123456)
                print(catalog_id)

        Notes:
            operationId ``ImBase_GetCatalogIdByObjectId``; путь
            ``GET /core/api/imbase/object/{objectId}/catalog/id`` (возвращает ``int64``).
        """
        data = await self._request("get", f"/core/api/imbase/object/{object_id}/catalog/id")
        return int(data)
