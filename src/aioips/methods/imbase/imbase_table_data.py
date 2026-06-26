"""Метод получения данных табличной части справочника IMBASE."""

from typing import Any

from ...core import APIManager


class ImBaseTableDataMixin(APIManager):
    """Реализует ``GET /core/api/imbase/table/{objectVersionId}`` (``ImBase_GetTableData``)."""

    async def imbase_table_data(
        self: "ImBaseTableDataMixin",
        object_version_id: int,
    ) -> dict[str, Any]:
        """Возвращает данные табличной части справочника IMBASE для версии объекта.

        Табличная часть справочника IMBASE — это набор строк-записей с колонками,
        привязанный к конкретной ВЕРСИИ объекта-справочника. Метод отдаёт полный снимок
        таблицы: описание колонок, строки-записи и сопутствующие метаданные.

        Когда применять: чтобы прочитать содержимое таблицы справочника для отображения
        или дальнейшей обработки. Настройки показа колонок — :meth:`imbase_table_display_settings`,
        пользовательский фильтр — :meth:`imbase_table_user_filter`. Предусловий нет
        (операция чтения).

        Args:
            object_version_id: Идентификатор ВЕРСИИ объекта-справочника (F_ID / поле ``id``
                DTO, НЕ ``objectID`` объекта). Версия задаёт конкретный снимок таблицы.

        Returns:
            Опаковая (нетипизированная) структура таблицы как ``dict[str, Any]`` по DTO
            ``TableDataDto``: колонки, строки и метаданные. Структура крупная и
            неоднородная, поэтому детально не типизируется. Пустой ``dict`` — если сервер
            вернул не-объект.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                table = await ips.imbase_table_data(7)  # 7 = id ВЕРСИИ
                print(table.get("columns"), table.get("rows"))

        Notes:
            operationId ``ImBase_GetTableData``; путь
            ``GET /core/api/imbase/table/{objectVersionId}`` (``TableDataDto``, без
            result-обёртки). Связанные методы: :meth:`imbase_table_display_settings`,
            :meth:`imbase_table_user_filter`, :meth:`imbase_table_created_objects`.
        """
        data = await self._request("get", f"/core/api/imbase/table/{object_version_id}")
        return data if isinstance(data, dict) else {}
