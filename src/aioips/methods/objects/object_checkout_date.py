"""Метод получения даты извлечения объекта на редактирование."""

from ...core import APIManager


class ObjectCheckoutDateMixin(APIManager):
    """Реализует ``GET /core/api/objects/{objectId}/getCheckOutDate``.

    Соответствует операции ``Objects_GetCheckOutDate``.
    """

    async def object_checkout_date(
        self: "ObjectCheckoutDateMixin",
        object_id: int,
    ) -> str:
        """Возвращает дату извлечения объекта на редактирование (checkout).

        Когда объект извлечён на правку (``checkOut``), сервер фиксирует момент извлечения.
        Метод отдаёт эту дату как строку в том виде, как её сериализует IPS (ISO-подобный
        формат с временем в UTC). Применяйте для аудита блокировок: понять, когда и не
        слишком ли давно объект удерживается в checkout, в паре с ``checkout_by`` из
        :class:`ObjectDto`. Если объект НЕ извлечён, сервер возвращает значение по
        умолчанию (пустую/нулевую дату), а не ошибку. Только чтение — checkout не требуется.

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии (F_ID).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для всех
                версий. Не идентификатор версии (``id`` / F_ID).

        Returns:
            Дата извлечения как строка (в формате IPS). Сервер возвращает строку всегда;
            для не извлечённого объекта это может быть нулевая/пустая дата.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                checked_out_at = await ips.object_checkout_date(102550)
                print(checked_out_at)

        Notes:
            ``operationId``: ``Objects_GetCheckOutDate``. Ответ — голая JSON-строка
            (``type: string``), не result-обёртка. Связано с :meth:`object_get`
            (поле ``checkout_by``). См. [[ips-object-model]] (раздел «Жизненный цикл»).
        """
        data = await self._request("get", f"/core/api/objects/{object_id}/getCheckOutDate")
        return str(data)
