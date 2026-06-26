"""Метод проверки существования типа атрибута по идентификатору."""

from ...core import APIManager


class AttributeTypeExistsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeTypes/{id}/exists``."""

    async def attribute_type_exists(
        self: "AttributeTypeExistsMixin",
        attribute_type_id: int,
    ) -> bool:
        """Проверяет существование типа атрибута по его идентификатору.

        Быстрый булев флаг: зарегистрирован ли в метаданных тип атрибута с заданным
        ``id``. Ответ сервера — голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: как дешёвый предварительный фильтр перед запросом полного
        метаописания (:meth:`attribute_type`) или чтением свойств — чтобы избежать
        обращений по заведомо отсутствующему ``id``. Аналог по GUID —
        :meth:`attribute_type_exists_by_guid`.

        Args:
            attribute_type_id: Идентификатор типа атрибута (id-пространство ТИПОВ
                атрибутов метаданных, не значение атрибута объекта).

        Returns:
            ``True`` — тип атрибута с таким ``id`` существует; ``False`` — не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.attribute_type_exists(1029):
                    attr = await ips.attribute_type(1029)

        Notes:
            operationId ``Metadata_ExistsAttributeTypeById``; путь
            ``GET /core/api/metadata/attributeTypes/{id}/exists`` (ответ — ``boolean``).
            Связанный метод: :meth:`attribute_type`.
        """
        path = f"/core/api/metadata/attributeTypes/{attribute_type_id}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
