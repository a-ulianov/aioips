"""Метод получения GUID типов объектов, участвующих в замещении."""

from ...core import APIManager


class SubstituteObjectTypeGuidsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/substitution/objectTypes/guids``."""

    async def substitute_object_type_guids(
        self: "SubstituteObjectTypeGuidsMixin",
    ) -> list[str]:
        """Возвращает GUID всех типов объектов, участвующих в замещении.

        Замещение — механизм IPS, в котором один объект замещает другой через специальные
        связи замещения (например, замена детали аналогом). Метод отдаёт плоский перечень
        стабильных GUID всех типов объектов, для которых определены отношения замещения.
        GUID переносимы между установками IPS (в отличие от ``id``), поэтому подходят для
        сверки конфигурации между средами. Ответ сервера — массив строк, без обёртки
        ``...NullableResultDto``.

        Когда применять: для сравнения наборов типов объектов с замещением между средами по
        стабильным GUID. Перечень числовых id — :meth:`substitute_object_type_ids`;
        проверка конкретного типа — :meth:`object_type_has_substitution_by_guid`.

        Returns:
            Список GUID типов объектов (строки в id-пространстве ТИПОВ объектов). Пустой
            список — типов объектов с замещением нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.substitute_object_type_guids()
                print(len(guids))

        Notes:
            operationId ``Metadata_GetSubstituteObjectGuids``; путь
            ``GET /core/api/metadata/substitution/objectTypes/guids`` (ответ — массив
            строк). Связанные методы: :meth:`substitute_object_type_ids`,
            :meth:`object_type_has_substitution_by_guid`.
        """
        path = "/core/api/metadata/substitution/objectTypes/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
