"""Метод получения id типов объектов, которые могут входить в чей-либо состав."""

from ...core import APIManager


class ObjectTypesWithEnterInApplicabilitiesIdsMixin(APIManager):
    """Реализует ``GET .../objectTypesWithEnterInApplicabilities/ids``."""

    async def object_types_with_enter_in_applicabilities_ids(
        self: "ObjectTypesWithEnterInApplicabilitiesIdsMixin",
    ) -> list[int]:
        """Возвращает id всех типов объектов, которые могут входить в чей-либо состав.

        Плоский справочник: идентификаторы типов объектов, фигурирующих в применяемостях
        как ПОТОМКИ — то есть объекты которых можно вложить в состав какого-либо
        родителя. Это срез матрицы применяемостей по дочерней стороне, зеркальный к
        :meth:`object_types_with_applicabilities_ids` (родительская сторона). Ответ —
        голый массив целых (без обёртки ``...NullableResultDto``), поэтому метод всегда
        отдаёт список, а не ``None``.

        Когда применять: для быстрого построения множества «типы, которые куда-то
        вкладываются» (фильтрация кандидатов на добавление в состав) без выгрузки самих
        правил. Проверка одного типа-потомка — :meth:`can_enters_in`; список его
        конкретных родителей — :meth:`object_type_parent_applicabilities`.

        Returns:
            Список идентификаторов типов объектов (``ObjectTypeID``), у которых есть
            применяемости-потомка. Пустой список — таких типов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                child_type_ids = await ips.object_types_with_enter_in_applicabilities_ids()
                print(child_type_ids)

        Notes:
            operationId ``Metadata_GetObjectTypeIdsWithEnterInApplicabilities``; путь
            ``GET /core/api/metadata/applicabilities/``
            ``objectTypesWithEnterInApplicabilities/ids`` (голый массив ``int``). См.
            объектной модели IPS (раздел «Связи и состав»). Связанные методы:
            :meth:`object_types_with_applicabilities_ids`, :meth:`can_enters_in`.
        """
        path = "/core/api/metadata/applicabilities/objectTypesWithEnterInApplicabilities/ids"
        data = await self._request("get", path)
        items = data if isinstance(data, list) else []
        return [int(item) for item in items]
