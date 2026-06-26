"""Метод получения полного (иерархического) имени типа объекта."""

from ...core import APIManager


class ObjectTypeFullNameMixin(APIManager):
    """Реализует ``GET /core/api/metadata/objectTypes/{id}/fullName``."""

    async def object_type_full_name(
        self: "ObjectTypeFullNameMixin",
        object_type_id: int,
    ) -> str:
        """Возвращает полное (иерархическое) имя типа объекта по идентификатору.

        Полное имя (``fullName``) отражает положение типа в иерархии типов объектов —
        путь по родительским типам, а не короткое системное имя
        (:meth:`object_type_name`) и не отображаемое имя экземпляра по умолчанию
        (:meth:`object_type_object_name`). Ответ сервера — голая строка, без обёртки
        ``...NullableResultDto``.

        Когда применять: для отображения типа с учётом его места в иерархии (деревья
        типов, выпадающие списки, диагностика), когда короткого имени недостаточно.

        Args:
            object_type_id: Идентификатор типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID``).

        Returns:
            Полное иерархическое имя типа объекта строкой; пустая строка, если сервер
            вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                full_name = await ips.object_type_full_name(1742)
                print(full_name)

        Notes:
            operationId ``Metadata_GetObjectTypeFullName``; путь
            ``GET /core/api/metadata/objectTypes/{id}/fullName``.
            Связанные методы: :meth:`object_type_name` (системное имя),
            :meth:`object_type_object_name` (имя экземпляра по умолчанию).
        """
        path = f"/core/api/metadata/objectTypes/{object_type_id}/fullName"
        data = await self._request("get", path)
        return "" if data is None else str(data)
