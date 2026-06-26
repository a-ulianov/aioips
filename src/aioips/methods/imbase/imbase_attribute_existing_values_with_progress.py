"""Метод поиска существующих значений атрибута IMBASE с прогресс-стримом (чтение)."""

from typing import Any

from ...core import APIManager
from ...schemas.imbase.table_search_params import ImBaseTableSearchParams


class ImBaseAttributeExistingValuesWithProgressMixin(APIManager):
    """Реализует ``POST .../imbase/attribute/byGuid/{attributeGuid}/existingValues/withProgress``.

    operationId ``ImBase_GetTableSearchExistingAttributeValuesWithProgress``.
    """

    async def imbase_get_table_search_existing_attribute_values_with_progress(
        self: "ImBaseAttributeExistingValuesWithProgressMixin",
        attribute_guid: str,
        params: ImBaseTableSearchParams,
        *,
        progress_report_step: int | None = None,
    ) -> None:
        """Ищет существующие значения атрибута IMBASE с отчётом о прогрессе (ЧТЕНИЕ).

        Прогресс-вариант :meth:`imbase_attribute_existing_values`: собирает
        фактически встречающиеся значения атрибута (по его GUID) в заданной области
        таблиц IMBASE, периодически репортя прогресс. Несмотря на HTTP-метод POST,
        это операция ЧТЕНИЯ — сервер ничего не изменяет; тело — контейнер параметров.

        Когда применять: для долгого сбора уникальных значений атрибута по большой
        выборке, когда нужен прогресс-репорт (UI-индикатор). Для быстрого случая без
        прогресса используйте :meth:`imbase_attribute_existing_values`.

        Предусловий нет (операция чтения). Эндпоинт ничего не возвращает телом —
        результат/прогресс доставляется отдельным каналом (прогресс-стрим), а сам
        ответ HTTP пуст (void).

        Args:
            attribute_guid: GUID ТИПА атрибута IMBASE, чьи значения ищем (id-пространство
                типов атрибутов — GUID, не числовой id); подставляется в путь URL.
            params: Параметры поиска (:class:`ImBaseTableSearchParams`): область
                ``table_links_lookup`` (id таблицы → id записей) и условия
                ``conditions``.
            progress_report_step: Шаг отчёта о прогрессе (query ``progressReportStep``);
                ``None`` — параметр не передаётся (серверный дефолт).

        Returns:
            ``None`` — сервер отвечает без тела (HTTP 200, void; прогресс/результат —
            вне тела ответа). Успех = отсутствие исключения.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                params = ImBaseTableSearchParams(table_links_lookup={"204": [1, 2, 3]})
                await ips.imbase_get_table_search_existing_attribute_values_with_progress(
                    "8f3c2a10-0000-0000-0000-000000000000", params, progress_report_step=10
                )

        Notes:
            operationId ``ImBase_GetTableSearchExistingAttributeValuesWithProgress``;
            путь ``POST .../imbase/attribute/byGuid/{attributeGuid}/existingValues
            /withProgress``; тело ``ImBaseTableSearchParamsDto``; ответ пуст (void).
            Связанные: :meth:`imbase_attribute_existing_values`. См. [[ips-object-model]].
        """
        payload = params.model_dump(mode="json", by_alias=True, exclude_none=True)
        request_params: dict[str, Any] = {}
        if progress_report_step is not None:
            request_params["progressReportStep"] = str(progress_report_step)
        await self._request(
            "post",
            f"/core/api/imbase/attribute/byGuid/{attribute_guid}/existingValues/withProgress",
            json=payload,
            params=request_params,
        )
