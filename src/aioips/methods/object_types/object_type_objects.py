"""Метод получения кратких сведений об объектах (экземплярах) заданного типа."""

from ...core import APIManager
from ...schemas.objects import QuickObjectInfo


class ObjectTypeObjectsMixin(APIManager):
    """Реализует метод ``GET /core/api/objectTypes/{objectTypeId}/objects``."""

    async def object_type_objects(
        self: "ObjectTypeObjectsMixin",
        object_type_id: int,
    ) -> list[QuickObjectInfo]:
        """Возвращает краткие сведения обо всех РЕАЛЬНЫХ объектах (экземплярах) типа.

        Перечисляет объекты указанного типа в виде облегчённых записей
        :class:`QuickObjectInfo` (id версии, id объекта, тип, заголовок). Это
        ЭКЗЕМПЛЯРЫ типа (реальные объекты), а не метаопределение: раздел ``objectTypes``
        отдаёт фактические объекты, тогда как раздел ``metadata`` (``ImsObjectTypeDto``)
        описывает метамодель.

        Когда применять: когда нужно обойти все объекты типа с заголовками — например
        показать список документов определённого вида. Если достаточно одних id —
        дешевле :meth:`object_type_object_ids`. За полным описанием конкретного объекта
        обращайтесь к ``object_get`` по полю ``object_id`` элемента результата.

        ВНИМАНИЕ: метод возвращает ВСЕ объекты типа без пагинации, поэтому для массовых
        типов ответ может быть очень большим (дорого по памяти/трафику). Для выборочного
        поиска предпочтительнее ``objects_select`` с условиями.

        Args:
            object_type_id: Идентификатор ТИПА объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ, не ``ObjectID``/``ID`` конкретного объекта или
                версии).

        Returns:
            Список :class:`QuickObjectInfo`. Пустой список означает, что объектов
            данного типа нет. У каждого элемента ``object_id`` (=``objectID``) —
            идентификатор объекта (F_OBJECT_ID), ``id`` — идентификатор версии (F_ID).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                items = await ips.object_type_objects(1742)
                for item in items:
                    print(item.object_id, item.caption)

        Notes:
            operationId ``Objects_GetObjectsByObjectTypeId``; путь
            ``GET /core/api/objectTypes/{objectTypeId}/objects`` (массив
            ``QuickObjectInfoDto``). Различие id/версия — см. [[ips-object-model]].
        """
        path = f"/core/api/objectTypes/{object_type_id}/objects"
        data = await self._request("get", path)
        return [QuickObjectInfo.model_validate(item) for item in data]
