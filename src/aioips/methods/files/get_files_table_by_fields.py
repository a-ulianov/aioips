"""Метод выборки таблицы файлов по объектам и выбранным колонкам (сервис имён)."""

from typing import Any

from ...core import APIManager
from ...schemas.files.data_table import DataTableDto
from ...schemas.files.files_table_params import ObjectIdsWithColumnsDto


class GetFilesTableByFieldsMixin(APIManager):
    """Реализует ``POST /core/api/files/fileNamesService/getFilesTableByFields``.

    operationId ``Files_GetFilesTableByFields``.
    """

    async def get_files_table_by_fields(
        self: "GetFilesTableByFieldsMixin",
        body: ObjectIdsWithColumnsDto | dict[str, Any],
    ) -> DataTableDto:
        """Возвращает таблицу файлов заданных объектов с выбранными колонками.

        Применяют, когда нужна таблица файлов по конкретному набору ОБЪЕКТОВ с
        управляемым составом колонок (полей) результата. Тело описывает оба
        входа: список объектов и имена колонок (см.
        :class:`ObjectIdsWithColumnsDto`).

        Это операция ЧТЕНИЯ. Несмотря на метод POST, данные не изменяются.

        Предусловие по id-пространству: ``objectIds`` в теле — ``ObjectID``
        (F_OBJECT_ID), а не ``id`` версий.

        Args:
            body: Параметры выборки — :class:`ObjectIdsWithColumnsDto` или
                эквивалентный ``dict`` (ключи ``objectIds``, ``columnNames``).
                Схема сериализуется как
                ``model_dump(mode="json", by_alias=True, exclude_none=True)``;
                ``dict`` отправляется как есть.

        Returns:
            :class:`DataTableDto` — ``columns`` (имена колонок) и ``rows``
            (строки-массивы значений ячеек, выровненные по колонкам). Пустые
            ``rows`` — совпадений нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.files import ObjectIdsWithColumnsDto

            async with IPSClient(config=config) as ips:
                table = await ips.get_files_table_by_fields(
                    ObjectIdsWithColumnsDto(
                        object_ids=[102550], column_names=["FileName", "BlobId"]
                    )
                )

        Notes:
            operationId ``Files_GetFilesTableByFields``. Часть сервиса имён
            файлов (``fileNamesService``). Связанные методы:
            :meth:`get_files_table_all_attributes`,
            :meth:`get_files_table_with_snapshot_ids`.
        """
        payload = (
            body.model_dump(mode="json", by_alias=True, exclude_none=True)
            if isinstance(body, ObjectIdsWithColumnsDto)
            else body
        )
        data = await self._request(
            "post",
            "/core/api/files/fileNamesService/getFilesTableByFields",
            json=payload,
        )
        return DataTableDto.model_validate(data if isinstance(data, dict) else {})
