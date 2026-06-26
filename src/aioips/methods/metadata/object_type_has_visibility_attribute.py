"""Метод проверки наличия атрибута видимости у типа объекта по идентификатору."""

from ...core import APIManager


class ObjectTypeHasVisibilityAttributeMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/visibility/objectTypes/{id}/exists``."""

    async def object_type_has_visibility_attribute(
        self: "ObjectTypeHasVisibilityAttributeMixin",
        object_type_id: int,
    ) -> bool:
        """Проверяет, есть ли у типа объекта атрибут видимости (по идентификатору).

        Возвращает ``True``, если у типа объекта задан атрибут видимости (visibility) —
        то есть видимость его экземпляров управляется специальным атрибутом. Ответ
        сервера — голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: как дешёвый предварительный фильтр перед чтением/правкой атрибута
        видимости — чтобы не обращаться к типам, у которых его нет. Аналог по GUID —
        :meth:`object_type_has_visibility_attribute_by_guid`; полный перечень таких типов —
        :meth:`visibility_object_type_ids`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (id-пространство ТИПОВ объектов
                метаданных, не id объекта/версии).

        Returns:
            ``True`` — у типа есть атрибут видимости; ``False`` — нет (в том числе если
            сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.object_type_has_visibility_attribute(42):
                    ...

        Notes:
            operationId ``Metadata_HasObjectTypeVisibilityAttributeById``; путь
            ``GET /core/api/metadata/visibility/objectTypes/{id}/exists`` (ответ —
            ``boolean``). Связанные методы:
            :meth:`object_type_has_visibility_attribute_by_guid`,
            :meth:`visibility_object_type_ids`.
        """
        path = f"/core/api/metadata/visibility/objectTypes/{object_type_id}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
