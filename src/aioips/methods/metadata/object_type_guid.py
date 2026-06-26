"""Метод получения GUID типа объекта по идентификатору."""

from ...core import APIManager


class ObjectTypeGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/objectTypes/{id}/guid``."""

    async def object_type_guid(
        self: "ObjectTypeGuidMixin",
        object_type_id: int,
    ) -> str:
        """Возвращает GUID типа объекта по его числовому идентификатору.

        Мост «локальный id → переносимый GUID»: числовой ``ObjectTypeID`` различается
        между инсталляциями, а GUID типа объекта стабилен между базами данных и удобен
        как переносимый ключ метаданных. Ответ сервера — голая строка GUID, без обёртки
        ``...NullableResultDto``.

        Когда применять: чтобы по локальному ``id`` типа получить его GUID для хранения
        переносимых ссылок или последующих вызовов ``...ByGuid`` (например
        :meth:`object_type_by_guid`, :meth:`object_type_id_by_guid`). Обратное
        преобразование — :meth:`object_type_id_by_guid`.

        Args:
            object_type_id: Идентификатор типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID``).

        Returns:
            GUID типа объекта строкой (например
            ``"cad001c5-306c-11d8-b4e9-00304f19f545"``); пустая строка, если сервер
            вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = await ips.object_type_guid(1742)
                print(guid)

        Notes:
            operationId ``Metadata_GetObjectTypeGuid``; путь
            ``GET /core/api/metadata/objectTypes/{id}/guid``.
            Обратное преобразование — :meth:`object_type_id_by_guid`.
        """
        path = f"/core/api/metadata/objectTypes/{object_type_id}/guid"
        data = await self._request("get", path)
        return "" if data is None else str(data)
