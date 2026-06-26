"""Метод получения объектов заданного типа."""

from ...core import APIManager
from ...schemas.objects import QuickObjectInfo


class ObjectsByObjectTypeMixin(APIManager):
    """Реализует метод ``GET /core/api/objectTypes/{objectTypeId}/objects``."""

    async def objects_by_object_type(
        self: "ObjectsByObjectTypeMixin",
        object_type_id: int,
    ) -> list[QuickObjectInfo]:
        """Возвращает краткие сведения обо всех объектах заданного типа.

        Перечисляет объекты, относящиеся к указанному типу (``ObjectTypeID``), в виде
        облегчённых записей :class:`QuickObjectInfo` (id версии, id объекта, тип,
        заголовок). Полезно для перебора/инвентаризации объектов одного типа без
        загрузки их атрибутов.

        Когда применять: когда нужно обойти все объекты типа — например, найти все
        документы определённого вида. ``object_type_id`` берётся из :meth:`object_types`
        или :meth:`object_type_id_by_name`. За полным описанием конкретного объекта
        обращайтесь к ``object_get`` по полю ``object_id`` элемента результата.

        ВНИМАНИЕ: метод возвращает ВСЕ объекты данного типа без пагинации, поэтому для
        массовых типов ответ может быть очень большим (дорого по памяти/трафику).
        Для выборочного поиска предпочтительнее ``objects_select`` с условиями.

        Args:
            object_type_id: Идентификатор типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` конкретного
                объекта или версии).

        Returns:
            Список :class:`QuickObjectInfo`. Пустой список означает, что объектов
            данного типа нет. У каждого элемента ``object_id`` (=``objectID``) —
            идентификатор объекта (F_OBJECT_ID), ``id`` — идентификатор версии (F_ID).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                items = await ips.objects_by_object_type(1742)
                for item in items:
                    print(item.object_id, item.caption)

        Notes:
            operationId ``Objects_GetObjectsByObjectTypeId``; путь
            ``GET /core/api/objectTypes/{objectTypeId}/objects`` (массив
            ``QuickObjectInfoDto``). Различие id/версия — см. [[ips-object-model]].
        """
        data = await self._request("get", f"/core/api/objectTypes/{object_type_id}/objects")
        return [QuickObjectInfo.model_validate(item) for item in data]
