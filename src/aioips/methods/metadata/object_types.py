"""Метод получения списка типов объектов метаданных."""

from ...core import APIManager
from ...schemas.metadata import ObjectType


class ObjectTypesMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/objectTypes``."""

    async def object_types(self: "ObjectTypesMixin") -> list[ObjectType]:
        """Возвращает список всех типов объектов, определённых в метаданных IPS.

        Тип объекта — это класс сущностей предметной области (документ, изделие, архив
        и т.д.); его идентификатор (``id``) задаёт «пространство типов объектов» и служит
        ключом во многих запросах. Метод отдаёт полный справочник типов одной выборкой.

        Когда применять: чтобы узнать ``id``/``guid`` нужного типа объекта перед вызовом
        методов, требующих ``objectTypeId`` — например :meth:`attribute_for_object_type_list`
        (какие атрибуты несёт тип) или при формировании условий поиска объектов.
        Предусловий нет (чтение справочника метаданных).

        Returns:
            Список типов объектов по схеме :class:`ObjectType`. Пустой список означает,
            что в базе не определено ни одного типа объекта.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                types = await ips.object_types()
                by_guid = {t.guid: t.object_name for t in types}

        Notes:
            operationId ``Metadata_GetObjectTypes``; путь
            ``GET /core/api/metadata/objectTypes`` (массив ``ImsObjectTypeDto``).
            Идентификатор типа объекта (``id``) — это ``ObjectTypeID``, отдельное
            id-пространство, не путать с ``ObjectID``/``ID`` конкретного объекта/версии.
            Связанные методы: :meth:`attribute_for_object_type_list`, :meth:`attribute_types`.
        """
        data = await self._request("get", "/core/api/metadata/objectTypes")
        return [ObjectType.model_validate(item) for item in data]
