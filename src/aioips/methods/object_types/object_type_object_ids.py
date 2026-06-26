"""Метод получения идентификаторов объектов (экземпляров) заданного типа."""

from ...core import APIManager


class ObjectTypeObjectIdsMixin(APIManager):
    """Реализует метод ``GET /core/api/objectTypes/{objectTypeId}/objectIds``."""

    async def object_type_object_ids(
        self: "ObjectTypeObjectIdsMixin",
        object_type_id: int,
    ) -> list[int]:
        """Возвращает идентификаторы всех РЕАЛЬНЫХ объектов (экземпляров) заданного типа.

        Перечисляет идентификаторы объектов, относящихся к указанному типу. Это
        ЭКЗЕМПЛЯРЫ типа (реальные объекты в базе), а не метаопределение типа — раздел
        ``objectTypes`` работает с фактическими объектами, тогда как раздел ``metadata``
        (``ImsObjectTypeDto``) описывает метамодель. Самый дешёвый способ узнать состав
        типа: возвращаются только числа, без атрибутов и заголовков.

        Когда применять: для перебора/инвентаризации всех объектов типа по id, например
        чтобы затем загрузить каждый через ``object_get``. Если нужны заголовки сразу —
        :meth:`object_type_objects` (вернёт :class:`QuickObjectInfo`). Для количества без
        перечня — :meth:`object_type_objects_info`. ``object_type_id`` берётся из
        :meth:`object_type_definition_by_name` или из раздела metadata.

        ВНИМАНИЕ: метод возвращает ВСЕ идентификаторы без пагинации; для массовых типов
        ответ может быть очень большим. Для выборки по условиям предпочтительнее
        ``objects_select``.

        Args:
            object_type_id: Идентификатор ТИПА объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ, не ``ObjectID``/``ID`` конкретного объекта или
                его версии).

        Returns:
            Список целочисленных идентификаторов объектов (``ObjectID``, F_OBJECT_ID).
            Пустой список означает, что объектов данного типа нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                object_ids = await ips.object_type_object_ids(1742)
                print(len(object_ids))

        Notes:
            operationId ``Objects_GetObjectIdsByObjectTypeId``; путь
            ``GET /core/api/objectTypes/{objectTypeId}/objectIds`` (массив ``int64``).
            Различие id объекта/версии — см. объектной модели IPS.
        """
        path = f"/core/api/objectTypes/{object_type_id}/objectIds"
        data = await self._request("get", path)
        return [int(item) for item in data]
