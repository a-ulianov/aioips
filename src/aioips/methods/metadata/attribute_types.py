"""Метод получения списка типов атрибутов метаданных."""

from ...core import APIManager
from ...schemas.metadata import AttributeType


class AttributeTypesMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeTypes``."""

    async def attribute_types(self: "AttributeTypesMixin") -> list[AttributeType]:
        """Возвращает список всех типов атрибутов, определённых в метаданных IPS.

        Тип атрибута описывает характеристику объекта: её тип данных (``FieldTypes`` —
        строка, число, дата, ссылка на объект, файл и т.д.), режим множественности
        значений и режим вычисляемости. Полный перечень типов атрибутов используется
        как справочник при работе со значениями атрибутов объектов в остальных
        разделах API.

        Когда применять: чтобы получить весь словарь атрибутов разом (например, построить
        отображение ``name → id`` или ``id → field_type``). Для точечного запроса по
        одному id/имени дешевле :meth:`attribute_type` / :meth:`attribute_type_id_by_name`;
        для атрибутов конкретного типа объекта — :meth:`attribute_for_object_type_list`.

        Returns:
            Список типов атрибутов по схеме :class:`AttributeType`. Пустой список
            означает, что в базе не определено ни одного типа атрибута.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                types = await ips.attribute_types()
                by_name = {t.name: t.id for t in types}

        Notes:
            operationId ``Metadata_GetAttributeTypes``; путь
            ``GET /core/api/metadata/attributeTypes`` (массив ``ImsAttributeTypeDto``).
        """
        data = await self._request("get", "/core/api/metadata/attributeTypes")
        return [AttributeType.model_validate(item) for item in data]
