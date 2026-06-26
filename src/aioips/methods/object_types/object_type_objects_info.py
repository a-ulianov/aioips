"""Метод получения сводки по объектам (экземплярам) заданного типа."""

from ...core import APIManager
from ...schemas.object_types import ObjectTypeObjectsInfo


class ObjectTypeObjectsInfoMixin(APIManager):
    """Реализует метод ``GET /core/api/objectTypes/{objectTypeId}/objectsInfo``."""

    async def object_type_objects_info(
        self: "ObjectTypeObjectsInfoMixin",
        object_type_id: int,
    ) -> ObjectTypeObjectsInfo:
        """Возвращает сводку (счётчики) по РЕАЛЬНЫМ объектам (экземплярам) заданного типа.

        Отдаёт агрегаты по ЭКЗЕМПЛЯРАМ типа: количество объектов и количество итераций
        (снимков) данного типа в базе. Это сведения о фактических объектах, а не о
        метамодели типа: раздел ``objectTypes`` оперирует реальными объектами, тогда
        как раздел ``metadata`` (``ImsObjectTypeDto``) описывает метаопределение.

        Когда применять: чтобы дёшево узнать «насколько массовый» данный тип, не
        перечисляя его объекты. Если нужны сами id — :meth:`object_type_object_ids`;
        если нужны записи с заголовками — :meth:`object_type_objects`. В отличие от
        большинства методов раздела, ответ НЕ обёрнут в ``...NullableResultDto`` —
        возвращается схема напрямую.

        Args:
            object_type_id: Идентификатор ТИПА объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ, не ``ObjectID``/``ID`` конкретного объекта или
                версии).

        Returns:
            Сводка по схеме :class:`ObjectTypeObjectsInfo`: ``objects_count`` —
            количество объектов, ``snapshots_count`` — количество итераций (снимков).
            Для типа без объектов счётчики равны 0.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                info = await ips.object_type_objects_info(1742)
                print(info.objects_count, info.snapshots_count)

        Notes:
            operationId ``ObjectTypes_GetObjectsInfo``; путь
            ``GET /core/api/objectTypes/{objectTypeId}/objectsInfo``
            (``ObjectTypeObjectsInfo``, без обёртки).
        """
        path = f"/core/api/objectTypes/{object_type_id}/objectsInfo"
        data = await self._request("get", path)
        return ObjectTypeObjectsInfo.model_validate(data)
