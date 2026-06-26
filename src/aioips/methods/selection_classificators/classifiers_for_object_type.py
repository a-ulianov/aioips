"""Метод получения классификаторов выбора, применимых к типу объекта."""

from ...core import APIManager


class ClassifiersForObjectTypeMixin(APIManager):
    """Реализует ``GET /core/api/selectionClassificators/byObjectTypeId/{objectTypeId}``.

    operationId ``SelectionClassificators_GetClassifierForObjType``.
    """

    async def classifiers_for_object_type(
        self: "ClassifiersForObjectTypeMixin",
        object_type_id: int,
    ) -> list[int]:
        """Возвращает идентификаторы классификаторов выбора, заданных для типа объекта.

        Классификатор выбора (selection classifier) — это справочник, ограничивающий выбор
        допустимых значений атрибута объекта: вместо свободного ввода значение берётся из
        заранее заданного классифицированного набора. К одному типу объекта может быть
        привязано несколько классификаторов; этот метод перечисляет их идентификаторы.

        Когда применять: как первый шаг работы с классификаторами для объектов данного типа —
        получить список доступных классификаторов, чтобы затем по каждому загрузить
        ограниченные им значения атрибутов конкретного объекта через
        :meth:`classificator_attributes`.

        Предусловий нет. Идентификатор здесь — это ТИП объекта (id типа в справочнике типов),
        НЕ идентификатор конкретного объекта (F_OBJECT_ID) и НЕ id версии (F_ID).

        Args:
            object_type_id: Идентификатор ТИПА объекта (id типа в справочнике типов IPS),
                для которого запрашиваются привязанные классификаторы выбора.

        Returns:
            Список идентификаторов классификаторов (``int64``). Пустой список означает, что
            к данному типу объекта не привязано ни одного классификатора выбора.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                classifier_ids = await ips.classifiers_for_object_type(1100)
                for classifier_id in classifier_ids:
                    print(classifier_id)

        Notes:
            operationId ``SelectionClassificators_GetClassifierForObjType``; путь
            ``GET /core/api/selectionClassificators/byObjectTypeId/{objectTypeId}``. Ответ —
            голый массив ``int64`` без result-обёртки. Связанный метод —
            :meth:`classificator_attributes`. См. объектной модели IPS.
        """
        data = await self._request(
            "get",
            f"/core/api/selectionClassificators/byObjectTypeId/{object_type_id}",
        )
        return [int(item) for item in data]
