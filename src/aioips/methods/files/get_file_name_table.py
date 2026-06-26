"""Метод выборки таблицы имён файлов (сервис имён файлов IPS)."""

from typing import Any

from ...core import APIManager
from ...schemas.files.data_table import DataTableDto


class GetFileNameTableMixin(APIManager):
    """Реализует ``POST /core/api/files/fileNamesService/getFileNameTable``.

    operationId ``Files_GetFileNameTable``.
    """

    async def get_file_name_table(
        self: "GetFileNameTableMixin",
        *,
        file_name: str | None = None,
    ) -> DataTableDto:
        """Возвращает таблицу метаданных имён файлов (опционально по образцу имени).

        Применяют для табличной выборки записей сервиса имён файлов IPS — обзора
        зарегистрированных имён файлов vault с их полями. Если задан
        ``file_name``, выборка ограничивается этим именем; иначе сервер применяет
        поведение по умолчанию.

        Это операция ЧТЕНИЯ. Несмотря на метод POST, тело не используется —
        образец имени передаётся в query; IPS требует наличия тела, поэтому
        отправляется пустой объект ``{}``.

        Args:
            file_name: Образец имени файла для фильтрации (query ``fileName``).
                ``None`` — параметр не передаётся (выборка по умолчанию).

        Returns:
            :class:`DataTableDto` — табличная выборка: ``columns`` (имена колонок)
            и ``rows`` (строки-массивы значений ячеек, выровненные по колонкам).
            Пустые ``rows`` — совпадений нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                table = await ips.get_file_name_table(file_name="schema.pdf")
                idx = table.columns.index("FileName")
                names = [row[idx] for row in table.rows]

        Notes:
            operationId ``Files_GetFileNameTable``. Часть сервиса имён файлов
            (``fileNamesService``). Возвращает метаданные ИМЁН файлов (не сами
            файлы). Связанные методы: :meth:`get_file_names_table`,
            :meth:`get_files_table`.
        """
        params: dict[str, Any] = {}
        if file_name is not None:
            params["fileName"] = str(file_name)
        data = await self._request(
            "post",
            "/core/api/files/fileNamesService/getFileNameTable",
            json={},
            params=params or None,
        )
        return DataTableDto.model_validate(data if isinstance(data, dict) else {})
