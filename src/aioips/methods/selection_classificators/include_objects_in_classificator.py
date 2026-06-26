"""Метод включения нескольких объектов в один классификатор выбора."""

from ...core import APIManager


class IncludeObjectsInClassificatorMixin(APIManager):
    """Реализует ``POST /core/api/selectionClassificators/includeObjectsInClassificator``.

    operationId ``SelectionClassificators_IncludeObjectsInClassificator``.
    """

    async def include_objects_in_classificator(
        self: "IncludeObjectsInClassificatorMixin",
        classificator_id: int,
        object_ids: list[int],
    ) -> None:
        """Включает несколько объектов в один классификатор выбора (мутирующая).

        Привязывает перечисленные объекты к одному объекту-классификатору: после вызова
        каждый из объектов становится включённым (классифицированным) в этот классификатор.
        Это обратная по смыслу операция к :meth:`exclude_objects_from_classificator`.

        Когда применять: когда нужно наполнить один классификатор сразу набором объектов за
        один запрос. Если же объект один, а классификаторов несколько — используйте
        :meth:`include_object_in_classificators`.

        Предусловий по жизненному циклу нет — операция применяется к объектам целиком, не
        требует checkout. Идемпотентна по факту принадлежности.

        Args:
            classificator_id: Идентификатор объекта-классификатора (F_OBJECT_ID объекта,
                представляющего классификатор выбора), в который включаются объекты.
                Передаётся в теле как ``classificatorId``.
            object_ids: Идентификаторы включаемых объектов (F_OBJECT_ID, id ОБЪЕКТОВ, а не
                id версий F_ID). Передаются в теле как ``objectIds``.

        Returns:
            ``None`` — сервер возвращает ``void``; успехом считается отсутствие ошибки.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.include_objects_in_classificator(204, [102550, 102551])

        Notes:
            operationId ``SelectionClassificators_IncludeObjectsInClassificator``; путь
            ``POST /core/api/selectionClassificators/includeObjectsInClassificator``; тело —
            ``{"classificatorId": ..., "objectIds": [...]}``. Обратный метод —
            :meth:`exclude_objects_from_classificator`. См. объектной модели IPS.
        """
        await self._request(
            "post",
            "/core/api/selectionClassificators/includeObjectsInClassificator",
            json={"classificatorId": classificator_id, "objectIds": object_ids},
        )
        return None
