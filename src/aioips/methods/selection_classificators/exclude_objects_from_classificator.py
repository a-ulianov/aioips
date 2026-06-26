"""Метод исключения нескольких объектов из одного классификатора выбора."""

from ...core import APIManager


class ExcludeObjectsFromClassificatorMixin(APIManager):
    """Реализует ``POST /core/api/selectionClassificators/excludeObjectsFromClassificator``.

    operationId ``SelectionClassificators_ExcludeObjectsFromClassificator``.
    """

    async def exclude_objects_from_classificator(
        self: "ExcludeObjectsFromClassificatorMixin",
        classificator_id: int,
        object_ids: list[int],
        *,
        confirm: bool = False,
    ) -> None:
        """Исключает несколько объектов из одного классификатора выбора (мутирующая, защищена).

        Снимает привязку перечисленных объектов к одному объекту-классификатору: после
        вызова каждый из объектов перестаёт быть включённым в этот классификатор. Операция
        необратима (отмена возможна только обратным включением), поэтому защищена гейтом
        ``confirm``: без ``confirm=True`` запрос не отправляется и поднимается
        :class:`ValueError`.

        Когда применять: когда нужно удалить набор объектов из одного классификатора за один
        запрос. Обратная операция — :meth:`include_objects_in_classificator`.

        Предусловий по жизненному циклу нет — операция применяется к объектам целиком, не
        требует checkout.

        Args:
            classificator_id: Идентификатор объекта-классификатора (F_OBJECT_ID объекта,
                представляющего классификатор выбора), из которого исключаются объекты.
                Передаётся в теле как ``classificatorId``.
            object_ids: Идентификаторы исключаемых объектов (F_OBJECT_ID, id ОБЪЕКТОВ, а не
                id версий F_ID). Передаются в теле как ``objectIds``.
            confirm: Подтверждение необратимой операции. Без ``True`` метод не делает запрос.

        Returns:
            ``None`` — сервер возвращает ``void``; успехом считается отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.exclude_objects_from_classificator(204, [102550, 102551], confirm=True)

        Notes:
            operationId ``SelectionClassificators_ExcludeObjectsFromClassificator``; путь
            ``POST /core/api/selectionClassificators/excludeObjectsFromClassificator``; тело —
            ``{"classificatorId": ..., "objectIds": [...]}``. Обратный метод —
            :meth:`include_objects_in_classificator`. См. объектной модели IPS.
        """
        if confirm is not True:
            raise ValueError(
                "Исключение объектов из классификатора необратимо: "
                "передайте confirm=True для подтверждения"
            )
        await self._request(
            "post",
            "/core/api/selectionClassificators/excludeObjectsFromClassificator",
            json={"classificatorId": classificator_id, "objectIds": object_ids},
        )
        return None
