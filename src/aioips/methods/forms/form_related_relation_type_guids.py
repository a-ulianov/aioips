"""Метод получения GUID типов связей, связанных с формой."""

from ...core import APIManager


class FormRelatedRelationTypeGuidsMixin(APIManager):
    """Реализует ``GET /core/api/forms/{formId}/relatedRelationTypeGuidsForForm``.

    operationId ``Forms_GetRelatedRelationTypeGuidsForFormById``.
    """

    async def form_related_relation_type_guids(
        self: "FormRelatedRelationTypeGuidsMixin",
        form_id: int,
    ) -> list[str]:
        """Возвращает GUID типов связей, связанных с формой.

        Для формы определён набор типов связей (отношений), к которым она применима.
        Метод отдаёт их GUID строками.

        Предусловие по id-пространству: аргумент — идентификатор формы (``formId``).

        Когда применять: чтобы узнать, с какими типами связей ассоциирована форма.
        Аналог для типов объектов — :meth:`form_related_object_type_guids`.

        Args:
            form_id: Идентификатор формы (``formId``), для которой запрашиваются
                связанные типы связей.

        Returns:
            Список GUID типов связей (строки). Пустой список означает отсутствие
            связанных типов связей.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.form_related_relation_type_guids(102551)
                print(guids)

        Notes:
            operationId ``Forms_GetRelatedRelationTypeGuidsForFormById``; путь
            ``GET /core/api/forms/{formId}/relatedRelationTypeGuidsForForm``;
            ответ — массив строк.
        """
        data = await self._request(
            "get", f"/core/api/forms/{form_id}/relatedRelationTypeGuidsForForm"
        )
        return [str(item) for item in data]
