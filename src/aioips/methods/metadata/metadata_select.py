"""Метод табличной выборки из таблицы метаданных."""

from typing import Any

from ...core import APIManager
from ...schemas.files.data_table import DataTableDto


class MetadataSelectMixin(APIManager):
    """Реализует ``POST /core/api/metadata/select`` (``Metadata_SelectFromMetadataTable``)."""

    async def metadata_select(
        self: "MetadataSelectMixin",
        request: dict[str, Any],
    ) -> DataTableDto:
        """Выполняет SQL-подобную выборку из системной таблицы метаданных IPS.

        Низкоуровневый доступ к таблицам метамодели: возвращает указанные колонки строк
        заданной таблицы метаданных с простым фильтром равенства. Это операция ЧТЕНИЯ
        (POST-verb, но схема не изменяется) — аналог ``SELECT columns FROM table WHERE
        col = value``. Результат — обобщённая таблица :class:`DataTableDto` (имена колонок
        плюс строки-массивы ячеек).

        Когда применять: когда специализированные методы раздела metadata не покрывают
        нужный срез и требуется прочитать «сырые» строки конкретной таблицы метаданных по
        её имени. Для прикладных задач предпочтительнее типизированные методы (типы,
        атрибуты, применяемости) — этот метод низкоуровневый и зависит от имён таблиц/колонок.

        Args:
            request: Тело запроса по схеме ``SelectFromTableDto`` (передаётся как dict,
                сериализуется в JSON «как есть»):

                - ``tableName`` (str): имя таблицы метаданных.
                - ``resultColumns`` (list[str]): имена возвращаемых колонок.
                - ``whereEquals`` (dict[str, Any]): условие «равно» (имя колонки → значение);
                  условия объединяются по AND.

        Returns:
            :class:`DataTableDto` с полями ``columns`` (имена колонок в порядке ячеек) и
            ``rows`` (строки-массивы значений, выровненные по ``columns``). Пустые
            ``columns``/``rows`` — выборка ничего не вернула.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. неизвестная таблица/колонка).

        Example:
            async with IPSClient(config=config) as ips:
                table = await ips.metadata_select(
                    {
                        "tableName": "T_OBJECT_TYPES",
                        "resultColumns": ["F_ID", "F_NAME"],
                        "whereEquals": {"F_LOCAL": 1},
                    }
                )
                idx = table.columns.index("F_NAME")
                names = [row[idx] for row in table.rows]

        Notes:
            operationId ``Metadata_SelectFromMetadataTable``; путь
            ``POST /core/api/metadata/select`` (тело — ``SelectFromTableDto``; ответ —
            ``DataTableDto``). Схема ответа переиспользована из ``schemas.files.data_table``.
            См. объектной модели IPS.
        """
        data = await self._request("post", "/core/api/metadata/select", json=request)
        return DataTableDto.model_validate(data if isinstance(data, dict) else {})
