"""Метод обновления даты модификации контента объекта (мутация)."""

from ...core import APIManager


class ObjectSetModifyContentDateMixin(APIManager):
    """Реализует ``POST /core/api/objects/{objectId}/setModifyContentDate``.

    operationId ``Objects_SetModifyContentDate`` (в swagger ``operationId`` отсутствует).
    """

    async def object_set_modify_content_date(
        self: "ObjectSetModifyContentDateMixin",
        object_id: int,
        *,
        confirm: bool = False,
    ) -> None:
        """Помечает контент объекта изменённым, проставляя текущую дату модификации (МУТАЦИЯ).

        Обновляет служебную дату «модификации контента» объекта на серверное текущее
        время. Эта дата отражает момент последнего изменения содержимого объекта и
        используется механизмами синхронизации, кэширования и отслеживания изменений.
        Метод НЕ меняет атрибуты объекта — только переставляет временную метку, как если
        бы контент был только что изменён («touch»).

        Когда применять: чтобы форсировать переоценку объекта потребителями, ориентирующимися
        на дату модификации (например, инвалидировать кэш или вызвать повторную обработку),
        не внося реальных правок в атрибуты.

        Предусловие по id-пространству: аргумент — идентификатор ОБЪЕКТА (``objectID`` /
        F_OBJECT_ID, общий для версий), а не идентификатор версии (``id`` / F_ID).

        Обратимость: операция НЕОБРАТИМА в прямом смысле — прежнее значение даты сервером
        не возвращается и не восстанавливается этим методом. Поскольку она изменяет
        серверное состояние, защищена параметром ``confirm``.

        Args:
            object_id: Идентификатор объекта (``objectID`` / F_OBJECT_ID), которому
                проставляется новая дата модификации контента.
            confirm: Подтверждение операции записи. Без ``True`` запрос НЕ выполняется и
                поднимается :class:`ValueError` ещё до обращения к серверу.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если объект не найден).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.object_set_modify_content_date(102550, confirm=True)

        Notes:
            operationId ``Objects_SetModifyContentDate``; путь
            ``POST /core/api/objects/{objectId}/setModifyContentDate``. Тело и query не
            требуются (отправляется ``json={}``). См. объектной модели IPS.
        """
        if confirm is not True:
            raise ValueError(
                "object_set_modify_content_date меняет дату модификации контента объекта; "
                "передайте confirm=True",
            )
        await self._request("post", f"/core/api/objects/{object_id}/setModifyContentDate", json={})
        return None
