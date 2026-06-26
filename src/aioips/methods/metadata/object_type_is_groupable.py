"""Метод проверки группируемости типа объекта по id."""

from ...core import APIManager


class ObjectTypeIsGroupableMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/grouping/objectTypes/groupable/{id}/exists``."""

    async def object_type_is_groupable(
        self: "ObjectTypeIsGroupableMixin",
        object_type_id: int,
    ) -> bool:
        """Проверяет, можно ли группировать экземпляры типа объекта (по id).

        «Groupable» означает, что экземпляры типа могут быть СГРУППИРОВАНЫ (выступать
        сгруппированными потомками) через сгруппированные типы связей, в отличие от
        «grouping» (тип сам выполняет группировку, см. :meth:`object_type_has_grouping`).
        Ответ сервера — голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: как дешёвый фильтр перед операциями группировки экземпляров
        данного типа. Аналог по GUID — :meth:`object_type_is_groupable_by_guid`; полный
        перечень группируемых типов — :meth:`groupable_object_type_ids`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (id-пространство типов объектов
                метаданных, не id объекта/версии).

        Returns:
            ``True`` — у типа есть сгруппированные типы связей (экземпляры группируемы);
            ``False`` — нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.object_type_is_groupable(42):
                    ids = await ips.grouping_relation_type_ids()

        Notes:
            operationId ``Metadata_HasObjectTypeGroupedRelationTypesById``; путь
            ``GET /core/api/metadata/grouping/objectTypes/groupable/{id}/exists`` (ответ —
            ``boolean``). Связанные методы: :meth:`object_type_is_groupable_by_guid`,
            :meth:`groupable_object_type_ids`.
        """
        path = f"/core/api/metadata/grouping/objectTypes/groupable/{object_type_id}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
