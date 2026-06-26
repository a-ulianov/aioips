"""Метод получения id типов объектов, у которых настроены применяемости."""

from ...core import APIManager


class ObjectTypesWithApplicabilitiesIdsMixin(APIManager):
    """Реализует ``GET .../objectTypesWithApplicabilities/ids``."""

    async def object_types_with_applicabilities_ids(
        self: "ObjectTypesWithApplicabilitiesIdsMixin",
    ) -> list[int]:
        """Возвращает id всех типов объектов, у которых задана хотя бы одна применяемость.

        Плоский справочник: идентификаторы типов объектов, фигурирующих в применяемостях
        как РОДИТЕЛИ — то есть объекты которых могут иметь состав (в них что-то может
        входить). Это базовый, без направления «вверх», срез матрицы применяемостей по
        родительской стороне. Ответ — голый массив целых (без обёртки
        ``...NullableResultDto``), поэтому метод всегда отдаёт список, а не ``None``.

        Когда применять: для быстрого построения множества «типы, поддерживающие
        состав» (фильтрация UI/логики) без выгрузки самих правил
        (:meth:`applicabilities`). Зеркальный срез по потомкам —
        :meth:`object_types_with_enter_in_applicabilities_ids`. Проверка одного типа —
        :meth:`has_applicability`.

        Returns:
            Список идентификаторов типов объектов (``ObjectTypeID``), у которых есть
            применяемости-родителя. Пустой список — таких типов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                parent_type_ids = await ips.object_types_with_applicabilities_ids()
                print(parent_type_ids)

        Notes:
            operationId ``Metadata_GetObjectTypeIdsWithApplicabilities``; путь
            ``GET /core/api/metadata/applicabilities/objectTypesWithApplicabilities/ids``
            (голый массив ``int``). См. [[ips-object-model]] (раздел «Связи и состав»).
            Связанные методы: :meth:`object_types_with_enter_in_applicabilities_ids`,
            :meth:`has_applicability`.
        """
        path = "/core/api/metadata/applicabilities/objectTypesWithApplicabilities/ids"
        data = await self._request("get", path)
        items = data if isinstance(data, list) else []
        return [int(item) for item in items]
