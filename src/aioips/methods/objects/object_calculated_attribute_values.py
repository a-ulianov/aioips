"""Метод вычисления значений формульных атрибутов объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import AttributeValues


class ObjectCalculatedAttributeValuesMixin(APIManager):
    """Реализует ``POST /core/api/objects/{objectId}/attributes/getCalculatedValues``.

    Соответствует операции ``ObjectAttributes_GetCalculatedValues``.
    """

    async def object_calculated_attribute_values(
        self: "ObjectCalculatedAttributeValuesMixin",
        object_id: int,
        attribute_values: list[AttributeValues],
        *,
        modes: str | None = None,
    ) -> list[AttributeValues]:
        """Вычисляет значения формульных (computed) атрибутов объекта на лету.

        Применяйте, когда нужно получить результат вычисляемых атрибутов
        (``ComputeValueModes``) объекта по набору исходных значений — без сохранения
        в БД. Метод передаёт входные значения атрибутов, а сервер возвращает их с
        пересчитанными формульными значениями. Это POST, но БЕЗ мутаций: объект не
        изменяется, checkout не требуется (вычисление, а не запись — ср.
        :meth:`object_set_attribute_values`, которая пишет значения и требует checkout).

        Предусловие по id-пространству: ``object_id`` — это id ОБЪЕКТА
        (``objectID`` / F_OBJECT_ID), общий для всех версий, а НЕ ``id`` версии.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), для которого
                вычисляются формульные атрибуты. В пути эндпоинта — ``objectId``.
            attribute_values: Исходные значения атрибутов (см. :class:`AttributeValues`),
                от которых ведётся расчёт. Сериализуется в тело запроса как «голый»
                массив (без обёртки-объекта).
            modes: Флаги расчёта (enum-строка ``GetCalculatedValuesModes``). Если
                ``None`` (по умолчанию), query-параметр ``modes`` не передаётся
                (серверный режим по умолчанию).

        Returns:
            Список значений атрибутов по схеме :class:`AttributeValues` с
            пересчитанными формульными значениями (пустой список, если сервер ничего
            не вернул). У каждого: ``attribute_id``, ``attribute_type`` (``FieldTypes``),
            ``values``, ``compute_mode`` (``ComputeValueModes``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.objects import AttributeValues

            async with IPSClient(config=config) as ips:
                calc = await ips.object_calculated_attribute_values(
                    102550,
                    [AttributeValues(attribute_id=12, values=["550.07.305"])],
                )
                by_id = {v.attribute_id: v.values for v in calc}

        Notes:
            ``operationId``: ``ObjectAttributes_GetCalculatedValues``. Тело и ответ —
            «голые» массивы ``AttributeValuesDto`` (распаковка напрямую). См.
            :meth:`object_attributes_values` и [[ips-object-model]] (раздел «Атрибуты»).
        """
        payload = [
            av.model_dump(mode="json", by_alias=True, exclude_none=True) for av in attribute_values
        ]
        params: dict[str, Any] = {}
        if modes is not None:
            params["modes"] = modes
        data = await self._request(
            "post",
            f"/core/api/objects/{object_id}/attributes/getCalculatedValues",
            json=payload,
            params=params,
        )
        items = data if isinstance(data, list) else []
        return [AttributeValues.model_validate(item) for item in items]
