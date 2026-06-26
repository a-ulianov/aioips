"""Метод выборки таблицы файлов по списку имён (сервис имён файлов IPS)."""

from ...core import APIManager
from ...schemas.files.data_table import DataTableDto


class GetFileNamesTableMixin(APIManager):
    """Реализует ``POST /core/api/files/fileNamesService/getFileNamesTable``.

    operationId ``Files_GetFileNamesTable``.
    """

    async def get_file_names_table(
        self: "GetFileNamesTableMixin",
        file_names: list[str],
    ) -> DataTableDto:
        """Возвращает таблицу метаданных файлов по заданному списку имён.

        Применяют для пакетной табличной выборки записей сервиса имён файлов по
        набору конкретных имён файлов vault (один запрос вместо N одиночных).

        Это операция ЧТЕНИЯ. Тело запроса — голый JSON-массив строк (имён);
        данные на сервере не изменяются.

        Args:
            file_names: Список имён файлов (тело — массив строк). Пустой список
                допустим (вернётся пустая таблица).

        Returns:
            :class:`DataTableDto` — ``columns`` (имена колонок) и ``rows``
            (строки-массивы значений ячеек, выровненные по колонкам). Пустые
            ``rows`` — совпадений нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                table = await ips.get_file_names_table(["a.pdf", "b.pdf"])
                rows = table.rows  # по строке на найденное имя

        Notes:
            operationId ``Files_GetFileNamesTable``. Часть сервиса имён файлов
            (``fileNamesService``). Имена файлов — пространство имён файлов, не
            id. Связанные методы: :meth:`get_file_name_table`,
            :meth:`get_files_table`.
        """
        data = await self._request(
            "post",
            "/core/api/files/fileNamesService/getFileNamesTable",
            json=list(file_names),
        )
        return DataTableDto.model_validate(data if isinstance(data, dict) else {})
