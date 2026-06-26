"""Метод включения объекта в несколько классификаторов выбора."""

from ...core import APIManager


class IncludeObjectInClassificatorsMixin(APIManager):
    """Реализует ``POST /core/api/selectionClassificators/includeObjectInClassificators``.

    operationId ``SelectionClassificators_IncludeObjectInClassificators``.
    """

    async def include_object_in_classificators(
        self: "IncludeObjectInClassificatorsMixin",
        object_id: int,
        classificator_object_ids: list[int],
    ) -> None:
        """Включает один объект сразу в несколько классификаторов выбора (мутирующая).

        Привязывает указанный объект к перечисленным объектам-классификаторам: после
        вызова объект становится включённым (классифицированным) в каждый из них. Это
        обратная по смыслу операция к :meth:`exclude_object_from_classificators`.

        Когда применять: когда нужно поместить один и тот же объект в набор классификаторов
        за один запрос (например, отнести деталь к нескольким справочным разделам). Если
        классификатор один, удобнее :meth:`include_objects_in_classificator` (с одним
        элементом в списке объектов).

        Предусловий по жизненному циклу нет — операция применяется к объекту целиком, не
        требует checkout. Идемпотентна по факту принадлежности (повторное включение не
        создаёт дубликатов).

        Args:
            object_id: Идентификатор включаемого объекта (F_OBJECT_ID, id ОБЪЕКТА, а не id
                версии F_ID). Передаётся в теле как ``objectId``.
            classificator_object_ids: Идентификаторы объектов-классификаторов (F_OBJECT_ID
                объектов, представляющих классификаторы выбора), в которые включается объект.
                Передаются в теле как ``classificatorObjectIds``.

        Returns:
            ``None`` — сервер возвращает ``void``; успехом считается отсутствие ошибки.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.include_object_in_classificators(102550, [204, 205])

        Notes:
            operationId ``SelectionClassificators_IncludeObjectInClassificators``; путь
            ``POST /core/api/selectionClassificators/includeObjectInClassificators``; тело —
            ``{"objectId": ..., "classificatorObjectIds": [...]}``. Обратный метод —
            :meth:`exclude_object_from_classificators`. См. объектной модели IPS.
        """
        await self._request(
            "post",
            "/core/api/selectionClassificators/includeObjectInClassificators",
            json={"objectId": object_id, "classificatorObjectIds": classificator_object_ids},
        )
        return None
