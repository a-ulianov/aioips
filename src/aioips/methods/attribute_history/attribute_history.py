"""Метод чтения истории значений атрибута."""

from ...core import APIManager
from ...schemas.attribute_history import AttributeHistoryRequest, AttributeHistoryValue


class AttributeHistoryMixin(APIManager):
    """Реализует ``POST /core/api/attributeHistory/getHistory``.

    operationId — ``AtributeHistory_GetAttributeHistory`` (опечатка в swagger
    сохранена намеренно).
    """

    async def attribute_history(
        self: "AttributeHistoryMixin",
        request: AttributeHistoryRequest,
    ) -> list[AttributeHistoryValue]:
        """Возвращает историю изменений значения атрибута (кто/когда/какое значение).

        Читает журнал значений конкретного атрибута: последовательность состояний
        с указанием установленного значения, момента изменения и автора. Применяйте,
        чтобы проследить, как менялась характеристика объекта или связи во времени
        (аудит, восстановление прежнего значения, разбор расхождений).

        Область выборки задаётся телом запроса :class:`AttributeHistoryRequest`:
        какой атрибут (``attribute_id``), у объекта или связи (``is_relation``),
        конкретный носитель (``id`` / ``type_id``) и охват (``history_type`` —
        один носитель / все объекты типа / все объекты). Операция только читает и
        идемпотентна; для необратимого удаления истории — :meth:`delete_attribute_history`.

        Предусловие по id-пространству: ``request.id`` — идентификатор НОСИТЕЛЯ
        значения (для объекта это версия, F_ID; для связи — id связи), а не id типа
        атрибута. История доступна лишь для атрибутов, у которых включено сохранение
        истории (опции ``savePrivateHistory`` / ``saveCommonHistory``); иначе список
        будет пустым.

        Args:
            request: Тело запроса (:class:`AttributeHistoryRequest`), однозначно
                адресующее историю: ``attribute_id``, ``is_relation``, ``id``,
                ``type_id``, ``only_personal``, ``history_type``.

        Returns:
            Список элементов истории (:class:`AttributeHistoryValue`), по одному на
            зафиксированное изменение. Пустой список — история не ведётся для этого
            атрибута либо у носителя нет записей. У элемента: ``date`` (UTC), ``value``
            (текст значения) и ``user`` (автор изменения).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.attribute_history import AttributeHistoryRequest, HistoryType

            async with IPSClient(config=config) as ips:
                history = await ips.attribute_history(
                    AttributeHistoryRequest(
                        attribute_id=9,
                        id=102550,
                        type_id=1742,
                        history_type=HistoryType.FOR_OBJECT,
                    )
                )
                for record in history:
                    print(record.date, record.user, record.value)

        Notes:
            ``operationId``: ``AtributeHistory_GetAttributeHistory`` (в swagger одна
            ``t`` в ``Atribute`` — опечатка сервера). Ответ — «голый» JSON-массив
            ``AttributeHistoryValueDto``. Связанный метод: :meth:`delete_attribute_history`.
        """
        payload = request.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/attributeHistory/getHistory", json=payload)
        items = data if isinstance(data, list) else []
        return [AttributeHistoryValue.model_validate(item) for item in items]
