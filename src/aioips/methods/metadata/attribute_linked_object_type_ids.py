"""Метод получения id типов объектов, на которые ссылается атрибут-ссылка."""

from ...core import APIManager


class AttributeLinkedObjectTypeIdsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeLinkedObjectTypeIds/{attributeTypeId}``."""

    async def attribute_linked_object_type_ids(
        self: "AttributeLinkedObjectTypeIdsMixin",
        attribute_type_id: int,
    ) -> list[int] | None:
        """Возвращает id типов объектов, на которые может ссылаться атрибут-ссылка.

        Для типа атрибута-ссылки (``ftObjectLink``) перечисляет допустимые типы объектов,
        на которые такой атрибут может указывать. Например, атрибут «Архив» (id 1029)
        ссылается на объекты-архивы — здесь вернутся id соответствующих типов объектов.
        Ответ обёрнут в ``Int32ListNullableResultDto`` (``{entity, isEntityPresent}``);
        обёртка разворачивается здесь, наружу отдаётся список ``id`` либо ``None``.

        Когда применять: чтобы узнать целевые типы атрибута-ссылки (валидация значения
        ссылки, построение UI выбора). Имеет смысл только для атрибутов-ссылок; для
        прочих типов ответ — пустой/``None``. Обратное направление (какие атрибуты-ссылки
        целятся в данный тип объекта) — :meth:`object_link_attribute_type_ids`.

        Args:
            attribute_type_id: Идентификатор ТИПА атрибута-ссылки (id-пространство типов
                атрибутов метаданных, не значение атрибута объекта).

        Returns:
            Список ``id`` типов объектов (id-пространство ТИПОВ объектов), на которые
            может ссылаться атрибут. ``None`` — сервер не вернул сущность
            (``isEntityPresent == false``); пустой список — целевых типов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                type_ids = await ips.attribute_linked_object_type_ids(1029)
                if type_ids:
                    print(type_ids)

        Notes:
            operationId ``Metadata_GetAttributeLinkedObjectTypeIds``; путь
            ``GET /core/api/metadata/attributeLinkedObjectTypeIds/{attributeTypeId}``
            (ответ — ``Int32ListNullableResultDto``). Связанные методы:
            :meth:`object_link_attribute_type_ids`, :meth:`attribute_supports_object_links`.
        """
        path = f"/core/api/metadata/attributeLinkedObjectTypeIds/{attribute_type_id}"
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return [int(item) for item in entity] if entity is not None else None
