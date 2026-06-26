"""Метод выборки таблицы файлов по списку id файлов (сервис имён файлов IPS)."""

from ...core import APIManager
from ...schemas.files.data_table import DataTableDto


class GetFilesTableMixin(APIManager):
    """Реализует ``POST /core/api/files/fileNamesService/getFilesTable``.

    operationId ``Files_GetFilesTable``.
    """

    async def get_files_table(
        self: "GetFilesTableMixin",
        file_ids: list[int],
    ) -> DataTableDto:
        """Возвращает таблицу метаданных файлов по списку идентификаторов файлов.

        Применяют для пакетной табличной выборки записей сервиса имён файлов по
        набору id файлов (одним запросом). Дополняет :meth:`get_file_names_table`
        (выборка по именам) — здесь ключом служат id файлов.

        Это операция ЧТЕНИЯ. Тело запроса — голый JSON-массив целых (id файлов);
        данные на сервере не изменяются.

        Предусловие по id-пространству: элементы ``file_ids`` — идентификаторы
        ФАЙЛОВ (пространство сервиса имён файлов, источник —
        :meth:`file_id_by_name`/:meth:`next_file_id`), а НЕ ``objectID`` объектов
        и не ``id`` версий.

        Args:
            file_ids: Список идентификаторов файлов (тело — массив int64). Пустой
                список допустим (вернётся пустая таблица).

        Returns:
            :class:`DataTableDto` — ``columns`` (имена колонок) и ``rows``
            (строки-массивы значений ячеек, выровненные по колонкам). Пустые
            ``rows`` — совпадений нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                table = await ips.get_files_table([778899, 778900])
                first = dict(zip(table.columns, table.rows[0]))

        Notes:
            operationId ``Files_GetFilesTable``. Часть сервиса имён файлов
            (``fileNamesService``). Связанные методы: :meth:`get_file_names_table`,
            :meth:`file_id_by_name`.
        """
        data = await self._request(
            "post",
            "/core/api/files/fileNamesService/getFilesTable",
            json=[int(x) for x in file_ids],
        )
        return DataTableDto.model_validate(data if isinstance(data, dict) else {})
