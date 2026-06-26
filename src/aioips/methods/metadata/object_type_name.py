"""Метод получения имени типа объекта по идентификатору."""

from ...core import APIManager


class ObjectTypeNameMixin(APIManager):
    """Реализует ``GET /core/api/metadata/objectTypes/{id}/name``."""

    async def object_type_name(
        self: "ObjectTypeNameMixin",
        object_type_id: int,
    ) -> str:
        """Возвращает системное имя типа объекта по его идентификатору.

        Системное имя (``objectTypeName``) — короткий идентификатор типа в метаданных
        (например ``"Document"``), не локализованное отображаемое имя экземпляра. Метод
        отдаёт только это имя, не загружая полное описание типа. Ответ сервера — голая
        строка, без обёртки ``...NullableResultDto``.

        Когда применять: чтобы по известному ``id`` типа получить лишь его системное
        имя (для логов, сопоставления, формирования путей), не вытягивая всю схему
        :meth:`object_type`. Имя экземпляра по умолчанию — :meth:`object_type_object_name`;
        полное иерархическое имя — :meth:`object_type_full_name`; аналог по GUID —
        :meth:`object_type_name_by_guid`.

        Args:
            object_type_id: Идентификатор типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID``).

        Returns:
            Системное имя типа объекта строкой; пустая строка, если сервер вернул
            ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                name = await ips.object_type_name(1742)
                print(name)  # "Document"

        Notes:
            operationId ``Metadata_GetObjectTypeNameById``; путь
            ``GET /core/api/metadata/objectTypes/{id}/name``.
            Связанные методы: :meth:`object_type_name_by_guid`,
            :meth:`object_type_object_name`, :meth:`object_type_full_name`.
        """
        path = f"/core/api/metadata/objectTypes/{object_type_id}/name"
        data = await self._request("get", path)
        return "" if data is None else str(data)
