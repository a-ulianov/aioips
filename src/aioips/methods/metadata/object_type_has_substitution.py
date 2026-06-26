"""Метод проверки наличия замещающих связей у типа объекта по id."""

from ...core import APIManager


class ObjectTypeHasSubstitutionMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/substitution/objectTypes/{id}/exists``."""

    async def object_type_has_substitution(
        self: "ObjectTypeHasSubstitutionMixin",
        id: int,
    ) -> bool:
        """Проверяет, есть ли у типа объекта замещающие типы связей (по id).

        Замещение — механизм IPS, в котором один объект замещает другой через специальные
        связи замещения. Метод отвечает, определены ли для типа объекта с данным ``id``
        типы связей замещения (то есть может ли объект этого типа участвовать в замещении).
        Ответ сервера — голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: как дешёвый предварительный фильтр перед обходом связей замещения
        у объектов данного типа. Аналог по GUID — :meth:`object_type_has_substitution_by_guid`;
        перечень всех таких типов — :meth:`substitute_object_type_ids`.

        Args:
            id: Идентификатор типа объекта (id-пространство ТИПОВ объектов метаданных,
                не id объекта и не id версии).

        Returns:
            ``True`` — у типа объекта есть замещающие типы связей; ``False`` — нет
            (в том числе если сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.object_type_has_substitution(42):
                    print("объекты этого типа можно замещать")

        Notes:
            operationId ``Metadata_HasObjectTypeSubstituteRelationTypesById``; путь
            ``GET /core/api/metadata/substitution/objectTypes/{id}/exists`` (ответ —
            ``boolean``). Связанные методы: :meth:`object_type_has_substitution_by_guid`,
            :meth:`substitute_object_type_ids`.
        """
        path = f"/core/api/metadata/substitution/objectTypes/{id}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
