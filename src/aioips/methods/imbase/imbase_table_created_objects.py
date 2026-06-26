"""Метод получения объектов, созданных из табличной части справочника IMBASE."""

from typing import Any

from ...core import APIManager


class ImBaseTableCreatedObjectsMixin(APIManager):
    """Реализует ``GET .../createdObjects`` (``ImBase_GetCreatedObjects``)."""

    async def imbase_table_created_objects(
        self: "ImBaseTableCreatedObjectsMixin",
        object_version_id: int,
    ) -> dict[str, Any] | None:
        """Возвращает объекты, созданные из записей табличной части справочника IMBASE.

        Записи таблицы справочника могут порождать объекты предметной области; метод
        возвращает соответствие «id записи → созданные объекты» для конкретной ВЕРСИИ
        объекта-справочника. Ответ обёрнут в ``...NullableResultDto``
        (``{entity, isEntityPresent}``); обёртка разворачивается здесь, наружу отдаётся
        либо словарь-соответствие, либо ``None``.

        Когда применять: чтобы узнать, какие объекты уже созданы по строкам таблицы
        справочника. Сами строки — :meth:`imbase_table_data`. Предусловий нет
        (операция чтения).

        Args:
            object_version_id: Идентификатор ВЕРСИИ объекта-справочника (F_ID / поле ``id``
                DTO, НЕ ``objectID`` объекта).

        Returns:
            Опаковый словарь-соответствие как ``dict[str, Any]`` по DTO
            ``Int64CreatedObjectInfoDtoIEnumerableIDictionary`` (ключ — id записи в виде
            строки, значение — список ``CreatedObjectInfoDto``), либо ``None``, если
            entity отсутствует (``isEntityPresent == false``). Структура неоднородная,
            детально не типизируется.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                created = await ips.imbase_table_created_objects(7)  # 7 = id ВЕРСИИ
                if created is not None:
                    for record_id, objects in created.items():
                        print(record_id, objects)

        Notes:
            operationId ``ImBase_GetCreatedObjects``; путь
            ``GET /core/api/imbase/table/{objectVersionId}/createdObjects``
            (``...IDictionaryNullableResultDto`` → entity). Связанные методы:
            :meth:`imbase_table_data`.
        """
        data = await self._request(
            "get",
            f"/core/api/imbase/table/{object_version_id}/createdObjects",
        )
        entity = data.get("entity") if isinstance(data, dict) else None
        return entity if isinstance(entity, dict) else None
