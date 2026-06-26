"""Метод получения идентификатора типа объекта по GUID."""

from urllib.parse import quote

from ...core import APIManager


class ObjectTypeIdByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/objectTypes/byGuid/{guid}/id``."""

    async def object_type_id_by_guid(
        self: "ObjectTypeIdByGuidMixin",
        guid: str,
    ) -> int:
        """Возвращает числовой идентификатор типа объекта по его GUID.

        Мост «переносимый GUID → локальный id»: GUID типа объекта стабилен между
        базами данных, а числовой ``ObjectTypeID`` различается между инсталляциями.
        Метод даёт локальный ``id``, нужный для запросов, принимающих ``objectTypeId``.
        Ответ сервера — целое число (идентификатор), а не объект-обёртка.

        Когда применять: чтобы по известному GUID типа получить его локальный ``id``
        перед вызовами вроде :meth:`object_type`, :meth:`objects_by_object_type` или
        :meth:`object_type_life_cycle_steps`. Аналог по имени — :meth:`object_type_id_by_name`.

        Args:
            guid: Глобальный идентификатор типа объекта (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Кодируется в URL.

        Returns:
            Числовой идентификатор типа объекта (``ObjectTypeID`` — id-пространство
            ТИПОВ объектов). Сервер не возвращает ``None``: при отсутствии GUID — ошибка.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если тип с таким GUID
                не найден).

        Example:
            async with IPSClient(config=config) as ips:
                type_id = await ips.object_type_id_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(type_id)

        Notes:
            operationId ``Metadata_GetObjectTypeId``; путь
            ``GET /core/api/metadata/objectTypes/byGuid/{guid}/id``.
            Связанные методы: :meth:`object_type`, :meth:`object_type_id_by_name`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/objectTypes/byGuid/{encoded_guid}/id"
        data = await self._request("get", path)
        return int(data)
