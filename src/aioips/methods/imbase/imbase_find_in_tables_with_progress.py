"""Метод поиска записей в таблицах IMBASE с прогресс-стримом (чтение через POST)."""

from typing import Any

from ...core import APIManager
from ...schemas.imbase.table_search_params import ImBaseTableSearchParams


class ImBaseFindInTablesWithProgressMixin(APIManager):
    """Реализует ``POST /core/api/imbase/find/inTables/withProgress``.

    operationId ``ImBase_FindInTablesWithProgress``.
    """

    async def imbase_find_in_tables_with_progress(
        self: "ImBaseFindInTablesWithProgressMixin",
        params: ImBaseTableSearchParams,
        *,
        progress_report_step: int | None = None,
    ) -> None:
        """Ищет записи в таблицах IMBASE по условиям с отчётом о прогрессе (ЧТЕНИЕ).

        Прогресс-вариант :meth:`imbase_find_in_tables`: ищет записи табличных частей
        справочника IMBASE по заданным условиям, периодически репортя прогресс.
        Несмотря на HTTP-метод POST, это операция ЧТЕНИЯ — сервер ничего не изменяет;
        тело служит контейнером параметров поиска.

        Когда применять: для долгого поиска по большой выборке таблиц IMBASE, когда
        нужен прогресс-репорт (UI-индикатор). Для быстрого случая без прогресса —
        :meth:`imbase_find_in_tables`.

        Предусловий нет (операция чтения). Эндпоинт ничего не возвращает телом —
        результат/прогресс доставляется отдельным каналом (прогресс-стрим), а сам
        ответ HTTP пуст (void).

        Args:
            params: Параметры поиска (:class:`ImBaseTableSearchParams`): область
                ``table_links_lookup`` (id таблицы → id записей) и условия
                фильтрации ``conditions``.
            progress_report_step: Шаг отчёта о прогрессе (query ``progressReportStep``);
                ``None`` — параметр не передаётся (серверный дефолт).

        Returns:
            ``None`` — сервер отвечает без тела (HTTP 200, void; прогресс/результат —
            вне тела ответа). Успех = отсутствие исключения.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                params = ImBaseTableSearchParams(
                    table_links_lookup={"204": [1, 2, 3]},
                    conditions=[{"attributeId": 1029, "condition": "eq", "data": "Сталь"}],
                )
                await ips.imbase_find_in_tables_with_progress(params, progress_report_step=25)

        Notes:
            operationId ``ImBase_FindInTablesWithProgress``; путь
            ``POST /core/api/imbase/find/inTables/withProgress``; тело
            ``ImBaseTableSearchParamsDto``; ответ пуст (void). Связанные:
            :meth:`imbase_find_in_tables`. См. [[ips-object-model]].
        """
        payload = params.model_dump(mode="json", by_alias=True, exclude_none=True)
        request_params: dict[str, Any] = {}
        if progress_report_step is not None:
            request_params["progressReportStep"] = str(progress_report_step)
        await self._request(
            "post",
            "/core/api/imbase/find/inTables/withProgress",
            json=payload,
            params=request_params,
        )
