"""Метод выборки таблицы файлов со всеми атрибутами (сервис имён файлов IPS)."""

from typing import Any

from ...core import APIManager
from ...schemas.files.data_table import DataTableDto
from ...schemas.files.files_table_params import ObjectIdsWithColumnsFileNameDto


class GetFilesTableAllAttributesMixin(APIManager):
    """Реализует ``POST /core/api/files/fileNamesService/getFilesTableAllAttributes``.

    operationId ``Files_GetFilesTableAllAttributes``.
    """

    async def get_files_table_all_attributes(
        self: "GetFilesTableAllAttributesMixin",
        body: ObjectIdsWithColumnsFileNameDto | dict[str, Any],
    ) -> DataTableDto:
        """Возвращает таблицу файлов объектов со всеми атрибутами (фильтр по имени).

        Расширение :meth:`get_files_table_by_fields`: помимо списка объектов и
        колонок принимает необязательный фильтр по имени файла и возвращает
        таблицу с полным набором атрибутов файлов (см.
        :class:`ObjectIdsWithColumnsFileNameDto`).

        Это операция ЧТЕНИЯ. Несмотря на метод POST, данные не изменяются.

        Предусловие по id-пространству: ``objectIds`` в теле — ``ObjectID``
        (F_OBJECT_ID), а не ``id`` версий.

        Args:
            body: Параметры выборки — :class:`ObjectIdsWithColumnsFileNameDto`
                или эквивалентный ``dict`` (ключи ``fileName``, ``objectIds``,
                ``columnNames``). Схема сериализуется как
                ``model_dump(mode="json", by_alias=True, exclude_none=True)``;
                ``dict`` отправляется как есть.

        Returns:
            :class:`DataTableDto` — ``columns`` (имена колонок) и ``rows``
            (строки-массивы значений ячеек). Пустые ``rows`` — совпадений нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.files import ObjectIdsWithColumnsFileNameDto

            async with IPSClient(config=config) as ips:
                table = await ips.get_files_table_all_attributes(
                    ObjectIdsWithColumnsFileNameDto(
                        object_ids=[102550], file_name="schema.pdf"
                    )
                )

        Notes:
            operationId ``Files_GetFilesTableAllAttributes``. Часть сервиса имён
            файлов (``fileNamesService``). Связанные методы:
            :meth:`get_files_table_by_fields`,
            :meth:`get_files_table_with_snapshot_ids`.
        """
        payload = (
            body.model_dump(mode="json", by_alias=True, exclude_none=True)
            if isinstance(body, ObjectIdsWithColumnsFileNameDto)
            else body
        )
        data = await self._request(
            "post",
            "/core/api/files/fileNamesService/getFilesTableAllAttributes",
            json=payload,
        )
        return DataTableDto.model_validate(data if isinstance(data, dict) else {})
