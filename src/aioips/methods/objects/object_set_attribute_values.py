"""Метод пакетной записи значений атрибутов объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import AttributeValues


class ObjectSetAttributeValuesMixin(APIManager):
    """Реализует ``ObjectAttributes_SetAttributeValues`` (запись значений атрибутов)."""

    async def object_set_attribute_values(
        self: "ObjectSetAttributeValuesMixin",
        object_id: int,
        attribute_values: list[AttributeValues],
        *,
        delete_not_existing: bool = False,
        dont_delete_blobs: bool = False,
        return_delta: bool = False,
        log_history: bool = True,
    ) -> list[AttributeValues]:
        """Записывает значения нескольких атрибутов объекта одним запросом.

        Основной способ изменить значения характеристик объекта (обозначение,
        наименование, ссылки и т.п.) пакетно. Применяйте, когда нужно установить или
        обновить значения уже известных атрибутов; для добавления временного атрибута
        используйте :meth:`object_add_temporary_attribute`, для полной замены набора
        атрибутов — :meth:`object_set_attributes`.

        ПРЕДУСЛОВИЕ (жизненный цикл): запись возможна, только если объект извлечён на
        редактирование (checkout). Этот метод НЕ делает checkout сам — это отдельная
        операция (``CheckOut`` → править → ``CheckIn``/``CancelChanges``). Если объект
        не в режиме редактирования, сервер вернёт ошибку (409 / конфликт ЖЦ). Запись
        также невозможна для атрибутов с ``read_only=True`` или в режиме ``cantModify``.

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для
                всех версий. Не идентификатор версии (``id`` / F_ID).
            attribute_values: Значения атрибутов для записи (см. :class:`AttributeValues`).
                У каждого элемента обязателен ``attribute_id`` (тип атрибута) и ``values``
                (для ``ftObjectLink`` — id объекта-цели). Сериализуются в тело запроса.
            delete_not_existing: Если ``True``, атрибуты объекта, не указанные в
                ``attribute_values``, будут удалены (полная замена набора). По умолчанию
                ``False`` (точечное обновление, прочие атрибуты сохраняются).
            dont_delete_blobs: Если ``True``, не удалять значения blob-атрибутов с диска
                при перезаписи. По умолчанию ``False``.
            return_delta: Если ``True``, сервер вернёт только реально изменившиеся
                значения (дельту); если ``False`` (по умолчанию) — вернёт полный набор
                записанных значений.
            log_history: Если ``True`` (по умолчанию), сервер фиксирует изменения в
                журнале истории модификаций (query ``isNeedToLogModificationHistory``).

        Returns:
            Список записанных значений атрибутов по схеме :class:`AttributeValues`
            (поле ``result`` ответа). При ``return_delta=True`` — только изменившиеся;
            при ``return_delta=False`` — полный набор. Журнал изменений
            (``modificationsHistory``) этим методом не возвращается.

        Raises:
            IPSConflictError: Если объект не извлечён на редактирование (конфликт ЖЦ).
            IPSForbiddenError: При отсутствии прав на запись атрибутов.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            from aioips.schemas.objects import AttributeValues

            async with IPSClient(config=config) as ips:
                # Объект 102550 предварительно извлечён на редактирование (checkout).
                written = await ips.object_set_attribute_values(
                    102550,
                    [AttributeValues(attribute_id=12, values=["550.07.305"])],
                )

        Notes:
            ``operationId``: ``ObjectAttributes_SetAttributeValues``. Тело запроса —
            ``SetAttributeValuesDto``; ответ — ``…WithLogInfoDto`` с полями ``result`` и
            ``modificationsHistory``. См. объектной модели IPS (раздел «Редактирование»)
            и граблям. Связанные методы: :meth:`object_set_attributes`,
            :meth:`object_attributes_values`.
        """
        payload: dict[str, Any] = {
            "attributeValues": [
                av.model_dump(mode="json", by_alias=True, exclude_none=True)
                for av in attribute_values
            ],
            "deleteNotExistingAttribute": delete_not_existing,
            "dontDeleteBlobs": dont_delete_blobs,
            "returnDelta": return_delta,
        }
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        data = await self._request(
            "post",
            f"/core/api/objects/{object_id}/attributeValues",
            json=payload,
            params=params,
        )
        result = data.get("result") if isinstance(data, dict) else None
        items = result if isinstance(result, list) else []
        return [AttributeValues.model_validate(item) for item in items]
