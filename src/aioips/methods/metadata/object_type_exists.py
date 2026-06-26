"""Метод проверки существования типа объекта по идентификатору."""

from ...core import APIManager


class ObjectTypeExistsMixin(APIManager):
    """Реализует ``GET /core/api/metadata/objectTypes/{id}/exists``."""

    async def object_type_exists(
        self: "ObjectTypeExistsMixin",
        object_type_id: int,
    ) -> bool:
        """Проверяет, существует ли тип объекта с указанным идентификатором.

        Дешёвый булев аксессор поверх «пространства типов объектов»: подтверждает,
        что в метаданных есть тип с данным ``ObjectTypeID``, не загружая его полное
        описание. Ответ сервера — голое булево значение, без обёртки
        ``...NullableResultDto``.

        Когда применять: как предварительный фильтр перед :meth:`object_type` или
        другими запросами по id типа, чтобы не дёргать тяжёлые методы для заведомо
        отсутствующих идентификаторов. Аналог по GUID — :meth:`object_type_exists_by_guid`.

        Args:
            object_type_id: Идентификатор типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` конкретного
                объекта или его версии).

        Returns:
            ``True`` — тип объекта с таким идентификатором существует; ``False`` — нет
            (в том числе если сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.object_type_exists(1742):
                    object_type = await ips.object_type(1742)

        Notes:
            operationId ``Metadata_ExistsObjectTypeById``; путь
            ``GET /core/api/metadata/objectTypes/{id}/exists`` (ответ — ``boolean``).
            Связанные методы: :meth:`object_type`, :meth:`object_type_exists_by_guid`.
        """
        path = f"/core/api/metadata/objectTypes/{object_type_id}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
