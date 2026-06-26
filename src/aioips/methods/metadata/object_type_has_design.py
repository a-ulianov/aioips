"""Метод проверки наличия проектируемой связи у типа объекта по идентификатору."""

from ...core import APIManager


class ObjectTypeHasDesignMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/design/objectTypes/{id}/exists``."""

    async def object_type_has_design(
        self: "ObjectTypeHasDesignMixin",
        object_type_id: int,
    ) -> bool:
        """Проверяет, есть ли у типа объекта проектируемый тип связи (по идентификатору).

        Возвращает ``True``, если для типа объекта задан хотя бы один проектируемый
        (designed) тип связи, то есть состав потомков такого типа можно проектировать.
        Ответ сервера — голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: как дешёвый предварительный фильтр перед операциями с
        конструкторским составом — чтобы не обращаться к типам, у которых проектируемых
        связей нет. Аналог по GUID — :meth:`object_type_has_design_by_guid`; полный
        перечень таких типов — :meth:`designed_object_type_ids`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (id-пространство ТИПОВ объектов
                метаданных, не id объекта/версии).

        Returns:
            ``True`` — у типа есть проектируемый тип связи; ``False`` — нет (в том числе
            если сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.object_type_has_design(42):
                    ...

        Notes:
            operationId ``Metadata_HasObjectTypeDesignedRelationTypeById``; путь
            ``GET /core/api/metadata/design/objectTypes/{id}/exists`` (ответ — ``boolean``).
            Связанные методы: :meth:`object_type_has_design_by_guid`,
            :meth:`designed_object_type_ids`.
        """
        path = f"/core/api/metadata/design/objectTypes/{object_type_id}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
