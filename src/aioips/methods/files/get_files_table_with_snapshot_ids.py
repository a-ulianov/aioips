"""Метод выборки таблицы файлов на момент снимков (сервис имён файлов IPS)."""

from typing import Any

from ...core import APIManager
from ...schemas.files.data_table import DataTableDto
from ...schemas.files.files_table_params import ObjectSnapshotIds


class GetFilesTableWithSnapshotIdsMixin(APIManager):
    """Реализует ``POST /core/api/files/fileNamesService/getFilesTableWithSnapshotIds``.

    operationId ``Files_GetFilesTableWithSnapshotIds``.
    """

    async def get_files_table_with_snapshot_ids(
        self: "GetFilesTableWithSnapshotIdsMixin",
        body: ObjectSnapshotIds | dict[str, Any],
    ) -> DataTableDto:
        """Возвращает таблицу файлов объектов в состоянии на момент снимков.

        Применяют, когда нужна таблица файлов не текущая, а зафиксированная на
        момент конкретных снимков (snapshot). Тело задаёт объекты и позиционно
        сопоставленные им идентификаторы снимков (см. :class:`ObjectSnapshotIds`).

        Это операция ЧТЕНИЯ. Несмотря на метод POST, данные не изменяются.

        Предусловие по id-пространству: ``objectIds`` — ``ObjectID``
        (F_OBJECT_ID); ``snapshotIds`` — идентификаторы СНИМКОВ (отдельное
        пространство id, не версии и не объекты).

        Args:
            body: Параметры выборки — :class:`ObjectSnapshotIds` или
                эквивалентный ``dict`` (ключи ``objectIds``, ``snapshotIds``).
                Схема сериализуется как
                ``model_dump(mode="json", by_alias=True, exclude_none=True)``;
                ``dict`` отправляется как есть.

        Returns:
            :class:`DataTableDto` — ``columns`` (имена колонок) и ``rows``
            (строки-массивы значений ячеек). Пустые ``rows`` — совпадений нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.files import ObjectSnapshotIds

            async with IPSClient(config=config) as ips:
                table = await ips.get_files_table_with_snapshot_ids(
                    ObjectSnapshotIds(object_ids=[102550], snapshot_ids=[5])
                )

        Notes:
            operationId ``Files_GetFilesTableWithSnapshotIds``. Часть сервиса
            имён файлов (``fileNamesService``). Связанные методы:
            :meth:`get_files_table_by_fields`,
            :meth:`get_files_table_all_attributes`.
        """
        payload = (
            body.model_dump(mode="json", by_alias=True, exclude_none=True)
            if isinstance(body, ObjectSnapshotIds)
            else body
        )
        data = await self._request(
            "post",
            "/core/api/files/fileNamesService/getFilesTableWithSnapshotIds",
            json=payload,
        )
        return DataTableDto.model_validate(data if isinstance(data, dict) else {})
