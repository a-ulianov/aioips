"""Метод получения сведений об использовании записи таблицы в табличных миксах."""

from typing import Any

from ...core import APIManager


class ImBaseTableRecordMixUsageMixin(APIManager):
    """Реализует ``GET .../table/{linkId}/records/{recordId}/tableMixUsage``.

    operationId ``ImBase_GetTableRecordTableMixUsageInfo``.
    """

    async def imbase_table_record_mix_usage(
        self: "ImBaseTableRecordMixUsageMixin",
        link_id: int,
        record_id: int,
    ) -> dict[str, Any] | None:
        """Возвращает сведения о вхождении записи таблицы в таблицы составных объектов.

        Запись ярлыка таблицы справочника может входить в «Таблицы составных объектов»
        (табличные миксы); метод отдаёт информацию об этих вхождениях для конкретной
        записи конкретной связи. Ответ обёрнут в ``...NullableResultDto``
        (``{entity, isEntityPresent}``); обёртка разворачивается здесь, наружу отдаётся
        либо словарь, либо ``None``.

        Когда применять: чтобы перед удалением/изменением записи понять, где она ещё
        используется (в каких таблицах составных объектов). Предусловий нет
        (операция чтения).

        Args:
            link_id: Идентификатор связи таблицы (``linkId``) — ярлык табличной части
                справочника.
            record_id: Идентификатор записи (``recordId``) внутри этой связи.

        Returns:
            Опаковая структура как ``dict[str, Any]`` по DTO
            ``TableRecordTableMixUsageInfoDto``, либо ``None``, если entity отсутствует
            (``isEntityPresent == false``). Структура неоднородная, детально не
            типизируется.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                usage = await ips.imbase_table_record_mix_usage(204, 1001)
                if usage is not None:
                    print(usage)

        Notes:
            operationId ``ImBase_GetTableRecordTableMixUsageInfo``; путь
            ``GET /core/api/imbase/table/{linkId}/records/{recordId}/tableMixUsage``
            (``...NullableResultDto`` → entity).
        """
        data = await self._request(
            "get",
            f"/core/api/imbase/table/{link_id}/records/{record_id}/tableMixUsage",
        )
        entity = data.get("entity") if isinstance(data, dict) else None
        return entity if isinstance(entity, dict) else None
