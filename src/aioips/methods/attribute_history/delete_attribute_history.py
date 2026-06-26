"""Метод удаления истории значений атрибута."""

from ...core import APIManager
from ...schemas.attribute_history import AttributeHistoryRequest


class DeleteAttributeHistoryMixin(APIManager):
    """Реализует ``POST /core/api/attributeHistory/deleteHistory``.

    operationId — ``AtributeHistory_DeleteHistory`` (опечатка в swagger
    сохранена намеренно). МУТИРУЮЩАЯ, необратимая операция.
    """

    async def delete_attribute_history(
        self: "DeleteAttributeHistoryMixin",
        request: AttributeHistoryRequest,
        *,
        confirm: bool = False,
    ) -> None:
        """Удаляет историю изменений значения атрибута (РАЗРУШАЮЩАЯ операция).

        МУТИРУЮЩИЙ метод: безвозвратно удаляет записи журнала значений атрибута.
        Восстановление невозможно, поэтому операция защищена confirm-гейтом — при
        ``confirm != True`` метод НЕ выполняет HTTP-запрос и сразу поднимает
        :class:`ValueError`. Перед удалением рекомендуется выгрузить историю через
        :meth:`attribute_history` (бэкап) согласно уставу §7.

        Область удаления задаётся телом :class:`AttributeHistoryRequest` и, что
        критично, полем ``history_type``: ``FOR_OBJECT`` — история одного носителя;
        ``FOR_SAME_TYPE`` — история по ВСЕМ объектам типа ``type_id``; ``FOR_ALL_TYPE`` —
        по ВСЕМ объектам. Два последних режима — массовые: убедитесь в значениях
        ``type_id``/``history_type``, прежде чем подтверждать.

        Предусловие по id-пространству: ``request.id`` — идентификатор НОСИТЕЛЯ
        значения (для объекта это версия, F_ID; для связи — id связи), а не id типа
        атрибута. ``only_personal=True`` ограничивает удаление персональной историей.

        Args:
            request: Тело запроса (:class:`AttributeHistoryRequest`), адресующее
                удаляемую историю: ``attribute_id``, ``is_relation``, ``id``,
                ``type_id``, ``only_personal``, ``history_type`` (область удаления).
            confirm: Гейт подтверждения необратимого действия. Должен быть ``True``,
                иначе метод не выполнит запрос и поднимет ``ValueError``.

        Returns:
            ``None``. При успехе сервер отвечает без содержимого (``204``/``200``).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт, до запроса).
            IPSForbiddenError: При отсутствии прав на удаление истории.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            from aioips.schemas.attribute_history import AttributeHistoryRequest, HistoryType

            async with IPSClient(config=config) as ips:
                await ips.delete_attribute_history(
                    AttributeHistoryRequest(
                        attribute_id=9,
                        id=102550,
                        type_id=1742,
                        history_type=HistoryType.FOR_OBJECT,
                    ),
                    confirm=True,
                )

        Notes:
            ``operationId``: ``AtributeHistory_DeleteHistory`` (в swagger одна ``t``
            в ``Atribute`` — опечатка сервера). См. устав §7 (confirm-гейты).
            Связанный метод: :meth:`attribute_history` (чтение перед удалением).
        """
        if confirm is not True:
            raise ValueError(
                "Удаление истории атрибута необратимо: передайте confirm=True для подтверждения"
            )
        payload = request.model_dump(mode="json", by_alias=True, exclude_none=True)
        await self._request("post", "/core/api/attributeHistory/deleteHistory", json=payload)
        return None
