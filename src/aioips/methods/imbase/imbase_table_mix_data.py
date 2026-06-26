"""Метод получения смешанных табличных данных объекта IMBASE (table mix)."""

from ...core import APIManager
from ...schemas.imbase.table_mix_data import TableMixDataDto


class ImBaseTableMixDataMixin(APIManager):
    """Реализует ``POST .../tableMix/{objectId}/data`` (``ImBase_GetTableMixData``)."""

    async def imbase_table_mix_data(
        self: "ImBaseTableMixDataMixin",
        object_id: int,
    ) -> TableMixDataDto:
        """Возвращает смешанные табличные данные (table mix) объекта IMBASE.

        «Таблица составного объекта» (table mix) сводит для одного объекта-справочника
        его рецептуры и входящие в них компоненты. Метод отдаёт двухуровневую
        структуру: словарь названий рецептур и словарь их состава. Это операция
        ЧТЕНИЯ: несмотря на метод POST и отсутствие тела, объект не изменяется.

        Когда применять: чтобы отобразить сводную таблицу рецептур/компонентов
        объекта. Тело запроса отсутствует — идентификатор передаётся в пути.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectId`` / ``ObjectID`` /
                F_OBJECT_ID, общий для версий, НЕ id версии), чьи смешанные
                табличные данные запрашиваются.

        Returns:
            Данные по схеме :class:`TableMixDataDto`: ``receptures``
            (``{id_рецептуры: название}``) и ``components``
            (``{id_рецептуры: [записи-компоненты]}``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                mix = await ips.imbase_table_mix_data(102550)
                for rec_id, title in mix.receptures.items():
                    print(title, len(mix.components.get(rec_id, [])))

        Notes:
            operationId ``ImBase_GetTableMixData``; путь
            ``POST /core/api/imbase/tableMix/{objectId}/data`` (без тела,
            ``TableMixDataDto`` без result-обёртки). Не путать с
            :meth:`imbase_table_record_mix_usage` (использование записи в миксах).
        """
        # Пустой ``json={}`` задаёт Content-Type application/json (иначе 415).
        data = await self._request("post", f"/core/api/imbase/tableMix/{object_id}/data", json={})
        return TableMixDataDto.model_validate(data)
