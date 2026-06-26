"""Метод исключения объекта из нескольких классификаторов выбора."""

from ...core import APIManager


class ExcludeObjectFromClassificatorsMixin(APIManager):
    """Реализует ``POST /core/api/selectionClassificators/excludeObjectFromClassificators``.

    operationId ``SelectionClassificators_ExcludeObjectFromClassificators``.
    """

    async def exclude_object_from_classificators(
        self: "ExcludeObjectFromClassificatorsMixin",
        object_id: int,
        classificator_object_ids: list[int],
        *,
        confirm: bool = False,
    ) -> None:
        """Исключает один объект из нескольких классификаторов выбора (мутирующая, защищена).

        Снимает привязку указанного объекта к перечисленным объектам-классификаторам: после
        вызова объект перестаёт быть включённым в каждый из них. Операция необратима (отмена
        возможна только обратным включением), поэтому защищена гейтом ``confirm``: без
        ``confirm=True`` запрос не отправляется и поднимается :class:`ValueError`.

        Когда применять: когда нужно удалить один объект из набора классификаторов за один
        запрос. Обратная операция — :meth:`include_object_in_classificators`.

        Предусловий по жизненному циклу нет — операция применяется к объекту целиком, не
        требует checkout.

        Args:
            object_id: Идентификатор исключаемого объекта (F_OBJECT_ID, id ОБЪЕКТА, а не id
                версии F_ID). Передаётся в теле как ``objectId``.
            classificator_object_ids: Идентификаторы объектов-классификаторов (F_OBJECT_ID
                объектов, представляющих классификаторы выбора), из которых исключается
                объект. Передаются в теле как ``classificatorObjectIds``.
            confirm: Подтверждение необратимой операции. Без ``True`` метод не делает запрос.

        Returns:
            ``None`` — сервер возвращает ``void``; успехом считается отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.exclude_object_from_classificators(102550, [204, 205], confirm=True)

        Notes:
            operationId ``SelectionClassificators_ExcludeObjectFromClassificators``; путь
            ``POST /core/api/selectionClassificators/excludeObjectFromClassificators``; тело —
            ``{"objectId": ..., "classificatorObjectIds": [...]}``. Обратный метод —
            :meth:`include_object_in_classificators`. См. объектной модели IPS.
        """
        if confirm is not True:
            raise ValueError(
                "Исключение объекта из классификаторов необратимо: "
                "передайте confirm=True для подтверждения"
            )
        await self._request(
            "post",
            "/core/api/selectionClassificators/excludeObjectFromClassificators",
            json={"objectId": object_id, "classificatorObjectIds": classificator_object_ids},
        )
        return None
