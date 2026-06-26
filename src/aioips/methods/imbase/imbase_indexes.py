"""Метод получения информации об индексах справочной системы IMBASE."""

from ...core import APIManager
from ...schemas.imbase import ImBaseIndexesInfo


class ImBaseIndexesMixin(APIManager):
    """Реализует ``GET /core/api/imbase/indexes`` (``ImBase_GetImBaseIndexesInfo``)."""

    async def imbase_indexes(self: "ImBaseIndexesMixin") -> ImBaseIndexesInfo:
        """Возвращает информацию об индексах справочной системы IMBASE.

        Отдаёт перечень каталогов, для которых заданы индексы, и список самих индексов
        (каждый — пара «каталог + проиндексированный атрибут»). Позволяет понять, по
        каким атрибутам каких каталогов возможен индексный поиск IMBASE.

        Когда применять: чтобы определить доступность индексного поиска перед его
        вызовом, либо построить карту «каталог → индексируемые атрибуты». Список
        каталогов целиком — :meth:`imbase_catalogs`; эти же данные входят в сводный
        снимок :meth:`imbase_client_cache_state` (поле ``indexes_info``). Предусловий
        нет (операция чтения).

        Returns:
            Информация об индексах по схеме :class:`ImBaseIndexesInfo`: ``catalogs``
            (каталоги с индексами) и ``indexes`` (пары «каталог + атрибут»). Пустые
            списки означают отсутствие индексов.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                info = await ips.imbase_indexes()
                for index in info.indexes:
                    print(index.catalog_id, index.attribute_id)

        Notes:
            operationId ``ImBase_GetImBaseIndexesInfo``; путь
            ``GET /core/api/imbase/indexes`` (``ImBaseIndexesInfoDto``, без
            result-обёртки).
        """
        data = await self._request("get", "/core/api/imbase/indexes")
        return ImBaseIndexesInfo.model_validate(data)
