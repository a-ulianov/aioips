"""Метод получения строкового представления значения атрибута объекта."""

from typing import Any

from ...core import APIManager


class ObjectAttributeAsStringMixin(APIManager):
    """Реализует ``ObjectAttributes_GetAttributeValueAsString`` (значение атрибута как строка)."""

    async def object_attribute_as_string(
        self: "ObjectAttributeAsStringMixin",
        object_id: int,
        attribute_id: int,
        *,
        throw_not_found: bool = False,
    ) -> str | None:
        """Возвращает значение атрибута объекта в виде готовой строки.

        Серверное строковое представление значения (то же, что ``as_string`` у
        :class:`Attribute`): IPS форматирует значение с учётом типа, единиц измерения и
        множественности. Применяйте, когда нужна только отображаемая строка, а не сами
        значения (:meth:`object_attribute_values`) или метаданные атрибута
        (:meth:`object_attribute`). Несмотря на метод POST, это операция чтения —
        checkout не нужен.

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для
                всех версий. Не идентификатор версии (``id`` / F_ID).
            attribute_id: Идентификатор ТИПА атрибута (какую характеристику читать).
            throw_not_found: Если ``True``, при отсутствии атрибута сервер вернёт ошибку
                (метод поднимет исключение); иначе метод вернёт ``None``.

        Returns:
            Строковое представление значения атрибута или ``None``, если сервер не вернул
            строку (например, атрибут отсутствует и ``throw_not_found`` равно ``False``).

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404 при ``throw_not_found``).

        Example:
            async with IPSClient(config=config) as ips:
                text = await ips.object_attribute_as_string(102550, 12)
                # text == "550.07.305"

        Notes:
            ``operationId``: ``ObjectAttributes_GetAttributeValueAsString``. Эндпоинт —
            POST с пустым телом ``{}``; ответ — голая JSON-строка (``type: string``), не
            result-обёртка. См. [[ips-object-model]] (раздел «Атрибуты»).
        """
        params: dict[str, Any] = {"throwNotFoundException": str(throw_not_found).lower()}
        data = await self._request(
            "post",
            f"/core/api/objects/{object_id}/attributes/{attribute_id}/asString",
            json={},
            params=params,
        )
        return data if isinstance(data, str) else None
