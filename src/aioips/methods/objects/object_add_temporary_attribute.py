"""Метод добавления временного атрибута объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import Attribute


class ObjectAddTemporaryAttributeMixin(APIManager):
    """Реализует ``ObjectAttributes_AddTemporaryAttribute`` (временный атрибут)."""

    async def object_add_temporary_attribute(
        self: "ObjectAddTemporaryAttributeMixin",
        object_id: int,
        attribute_id: int,
        *,
        fail_if_exists: bool = False,
        values: list[Any] | None = None,
    ) -> Attribute:
        """Добавляет объекту временный атрибут заданного типа.

        Временный атрибут существует в рамках текущего сеанса работы с объектом и
        используется, когда нужно прикрепить характеристику, не входящую в постоянный
        состав атрибутов типа. Для записи значений постоянных атрибутов применяйте
        :meth:`object_set_attribute_values`.

        ПРЕДУСЛОВИЕ (жизненный цикл): добавление возможно, только если объект извлечён на
        редактирование (checkout). Этот метод НЕ делает checkout сам — это отдельная
        операция (``CheckOut`` → править → ``CheckIn``/``CancelChanges``). Если объект
        не в режиме редактирования, сервер вернёт ошибку (409 / конфликт ЖЦ).

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для
                всех версий. Не идентификатор версии (``id`` / F_ID).
            attribute_id: Идентификатор ТИПА добавляемого временного атрибута.
            fail_if_exists: Если ``True`` и такой атрибут уже есть, сервер вернёт ошибку;
                если ``False`` (по умолчанию) — существующий атрибут переиспользуется.
            values: Значения временного атрибута (для ``ftObjectLink`` — id объекта-цели).
                ``None`` (по умолчанию) — атрибут без значений.

        Returns:
            Добавленный атрибут по схеме :class:`Attribute` (с присвоенными сервером
            метаданными). Ответ этого эндпоинта — голый ``AttributeDto``, без обёртки с
            журналом изменений.

        Raises:
            IPSConflictError: Если объект не извлечён на редактирование (конфликт ЖЦ),
                либо атрибут уже существует при ``fail_if_exists=True``.
            IPSForbiddenError: При отсутствии прав на изменение объекта.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                # Объект 102550 предварительно извлечён на редактирование (checkout).
                attr = await ips.object_add_temporary_attribute(
                    102550, 12, values=["временное значение"]
                )

        Notes:
            ``operationId``: ``ObjectAttributes_AddTemporaryAttribute``. Тело запроса —
            ``TempAttributeDto {attributeId, failIfExists, values}``. Эндпоинт не имеет
            параметра журналирования истории. См. [[ips-object-model]] (раздел «Атрибуты»).
            Связанные методы: :meth:`object_set_attribute_values`, :meth:`object_attributes`.
        """
        payload: dict[str, Any] = {
            "attributeId": attribute_id,
            "failIfExists": fail_if_exists,
            "values": values or [],
        }
        data = await self._request(
            "post",
            f"/core/api/objects/{object_id}/attributes/tempAttribute",
            json=payload,
        )
        return Attribute.model_validate(data)
