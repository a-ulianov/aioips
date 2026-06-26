"""Метод поиска объектов по типу и условиям на значения атрибутов."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import ObjectSelectResult, SelectCondition


class ObjectsSelectMixin(APIManager):
    """Реализует ``POST /core/api/objects/select`` (``Objects_GetSelectsObjects``)."""

    async def objects_select(
        self: "ObjectsSelectMixin",
        object_type_id: int,
        *,
        conditions: list[SelectCondition] | None = None,
        attribute_ids: list[int] | None = None,
        record_count: int | None = None,
        local_types_mode: bool = False,
        trash_mode: bool = False,
        last_key_value: int | None = None,
        last_order_value: list[Any] | None = None,
    ) -> list[ObjectSelectResult]:
        """Ищет объекты заданного типа по условиям на значения их атрибутов.

        Основной способ найти объекты, когда заранее не известны их идентификаторы:
        фильтрация по типу и значениям атрибутов. Найденные id затем передаются в
        :meth:`object_get` (как ``objectID``) для полного описания. Типичный кейс —
        найти все документы конкретного архива: членство в архиве задаётся
        атрибутом-ссылкой (``ftObjectLink``, в этой БД атрибут «Архив» = id 1029),
        а НЕ составом, поэтому ищется именно через ``objects_select`` с
        ``content=ID`` по id объекта-архива.

        Предусловия и грабли: для условия по атрибуту-ссылке сравнение ведётся по id
        связанного объекта (``content=ColumnContent.ID``). Результат зависит от контекста
        версий (правила фильтрации версий на сервере) — для воспроизводимости фиксируйте
        условия. Серверная пагинация — keyset, не offset; ``record_count`` ограничивает
        размер страницы.

        Args:
            object_type_id: Идентификатор типа искомых объектов (обязателен).
            conditions: Условия поиска по значениям атрибутов (см. :class:`SelectCondition`);
                объединяются логическими операторами самих условий. ``None`` или пустой
                список — без фильтра по атрибутам (только по типу).
            attribute_ids: Идентификаторы типов атрибутов, значения которых вернуть в
                результате для каждого объекта. ``None`` — значения атрибутов не возвращать.
            record_count: Ограничение на число возвращаемых записей (размер страницы).
                ``None`` — серверное значение по умолчанию.
            local_types_mode: Включить режим локальных типов объектов. По умолчанию ``False``.
            trash_mode: Искать среди удалённых объектов (в корзине). По умолчанию ``False``.
            last_key_value: Курсор keyset-пагинации — ``object_id`` ПОСЛЕДНЕГО объекта
                предыдущей страницы. Сервер вернёт записи «после» него (``lastKeyValue``).
                ``None`` — первая страница. Обычно задаётся не вручную, а хелпером
                :meth:`objects_select_iter`.
            last_order_value: Значения сортировочных колонок последней строки предыдущей
                страницы (``lastOrderValue``); нужно при пользовательской сортировке.
                ``None`` — не передаётся (keyset по умолчанию — по ``object_id``).

        Returns:
            Список совпадений по схеме :class:`ObjectSelectResult` (пустой список, если
            ничего не найдено). У каждого элемента — ``object_id`` найденного объекта и
            ``attributes`` (значения запрошенных в ``attribute_ids`` атрибутов).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.common.enumerations import RelationalOperator, ColumnContent
            from aioips.schemas.objects import SelectCondition

            async with IPSClient(config=config) as ips:
                # Все документы (тип 1742) в архиве с id 1240084 (атрибут-ссылка 1029).
                results = await ips.objects_select(
                    object_type_id=1742,
                    conditions=[SelectCondition(
                        attribute_id=1029,
                        relational_operator=RelationalOperator.EQUAL,
                        value=1240084,
                        content=ColumnContent.ID,
                    )],
                    attribute_ids=[9, 10],
                )
                object_ids = [r.object_id for r in results]

        Notes:
            ``operationId``: ``Objects_GetSelectsObjects``. См. [[ips-object-model]]
            (раздел «Поиск») и [[gotchas]]. Связанные методы: :meth:`object_get`,
            :meth:`object_composition_with_params`.
        """
        payload: dict[str, Any] = {
            "objectTypeId": object_type_id,
            "conditions": [
                c.model_dump(mode="json", by_alias=True, exclude_none=True)
                for c in (conditions or [])
            ],
            "attributeIdsToSelect": attribute_ids or [],
            "localTypesMode": local_types_mode,
            "trashMode": trash_mode,
        }
        if record_count is not None:
            payload["recordCount"] = record_count
        if last_key_value is not None:
            payload["lastKeyValue"] = last_key_value
        if last_order_value is not None:
            payload["lastOrderValue"] = last_order_value
        data = await self._request("post", "/core/api/objects/select", json=payload)
        items = data if isinstance(data, list) else []
        return [ObjectSelectResult.model_validate(item) for item in items]
