"""Метод записи набора атрибутов объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import Attribute


class ObjectSetAttributesMixin(APIManager):
    """Реализует ``ObjectAttributes_SetAttributes`` (запись набора атрибутов)."""

    async def object_set_attributes(
        self: "ObjectSetAttributesMixin",
        object_id: int,
        attributes: list[Attribute],
        *,
        log_history: bool = True,
    ) -> list[Attribute]:
        """Записывает набор атрибутов объекта (в формате DTO атрибутов).

        Применяйте, когда значения задаются полными DTO атрибутов (:class:`Attribute`,
        как их возвращает :meth:`object_attributes`) — например, при переносе атрибутов
        между объектами. Для записи значений по типу атрибута удобнее
        :meth:`object_set_attribute_values`; для добавления временного атрибута —
        :meth:`object_add_temporary_attribute`.

        ПРЕДУСЛОВИЕ (жизненный цикл): запись возможна, только если объект извлечён на
        редактирование (checkout). Этот метод НЕ делает checkout сам — это отдельная
        операция (``CheckOut`` → править → ``CheckIn``/``CancelChanges``). Если объект
        не в режиме редактирования, сервер вернёт ошибку (409 / конфликт ЖЦ).

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для
                всех версий. Не идентификатор версии (``id`` / F_ID).
            attributes: Атрибуты для записи (см. :class:`Attribute`). У каждого обязателен
                ``attribute_id`` (тип атрибута); ``values`` — значения (для ``ftObjectLink``
                — id объекта-цели). Сериализуются в тело-массив запроса.
            log_history: Если ``True`` (по умолчанию), сервер фиксирует изменения в
                журнале истории модификаций (query ``isNeedToLogModificationHistory``).

        Returns:
            Список записанных атрибутов по схеме :class:`Attribute` (поле ``result``
            ответа). Журнал изменений (``modificationsHistory``) этим методом не
            возвращается.

        Raises:
            IPSConflictError: Если объект не извлечён на редактирование (конфликт ЖЦ).
            IPSForbiddenError: При отсутствии прав на запись атрибутов.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            from aioips.schemas.objects import Attribute

            async with IPSClient(config=config) as ips:
                # Объект 102550 предварительно извлечён на редактирование (checkout).
                written = await ips.object_set_attributes(
                    102550,
                    [Attribute(attribute_id=12, values=["550.07.305"])],
                )

        Notes:
            ``operationId``: ``ObjectAttributes_SetAttributes``. Тело запроса — голый
            JSON-массив ``list[AttributeDto]``; ответ — ``…WithLogInfoDto`` с полями
            ``result`` и ``modificationsHistory``. См. [[ips-object-model]] (раздел
            «Редактирование»). Связанные методы: :meth:`object_set_attribute_values`,
            :meth:`object_attributes`.
        """
        body = [a.model_dump(mode="json", by_alias=True, exclude_none=True) for a in attributes]
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        data = await self._request(
            "post",
            f"/core/api/objects/{object_id}/attributes",
            json=body,
            params=params,
        )
        result = data.get("result") if isinstance(data, dict) else None
        items = result if isinstance(result, list) else []
        return [Attribute.model_validate(item) for item in items]
