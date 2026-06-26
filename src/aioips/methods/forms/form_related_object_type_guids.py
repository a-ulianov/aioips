"""Метод получения GUID типов объектов, связанных с формой."""

from ...core import APIManager


class FormRelatedObjectTypeGuidsMixin(APIManager):
    """Реализует ``GET /core/api/forms/{formId}/relatedObjectTypeGuidsForForm``.

    operationId ``Forms_GetRelatedObjectTypeGuidsForFormById``.
    """

    async def form_related_object_type_guids(
        self: "FormRelatedObjectTypeGuidsMixin",
        form_id: int,
    ) -> list[str]:
        """Возвращает GUID типов объектов, связанных с формой.

        Для формы определён набор типов объектов, к которым она применима/привязана.
        Метод отдаёт их GUID строками.

        Предусловие по id-пространству: аргумент — идентификатор формы (``formId``).

        Когда применять: чтобы узнать, с какими типами объектов ассоциирована форма
        (например, для проверки применимости). Аналог для типов связей —
        :meth:`form_related_relation_type_guids`.

        Args:
            form_id: Идентификатор формы (``formId``), для которой запрашиваются
                связанные типы объектов.

        Returns:
            Список GUID типов объектов (строки). Пустой список означает отсутствие
            связанных типов объектов.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.form_related_object_type_guids(102551)
                print(guids)

        Notes:
            operationId ``Forms_GetRelatedObjectTypeGuidsForFormById``; путь
            ``GET /core/api/forms/{formId}/relatedObjectTypeGuidsForForm``;
            ответ — массив строк.
        """
        data = await self._request(
            "get", f"/core/api/forms/{form_id}/relatedObjectTypeGuidsForForm"
        )
        return [str(item) for item in data]
