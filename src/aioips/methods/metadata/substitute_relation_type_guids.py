"""Метод получения GUID специальных типов связей замещения."""

from ...core import APIManager


class SubstituteRelationTypeGuidsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/substitution/relationTypes/guids``."""

    async def substitute_relation_type_guids(
        self: "SubstituteRelationTypeGuidsMixin",
    ) -> list[str]:
        """Возвращает GUID всех специальных типов связей замещения.

        Замещение реализуется через специальные типы СВЯЗЕЙ: объект-заместитель связан с
        замещаемым объектом связью особого типа. Метод отдаёт плоский перечень стабильных
        GUID всех таких типов связей замещения. GUID переносимы между установками IPS
        (в отличие от ``id``), поэтому подходят для сверки конфигурации между средами.
        Ответ сервера — массив строк, без обёртки ``...NullableResultDto``.

        Когда применять: для сравнения наборов типов связей замещения между средами по
        стабильным GUID. Перечень числовых id — :meth:`substitute_relation_type_ids`;
        проверка конкретного типа связи — :meth:`relation_type_has_substitutes_by_guid`.

        Returns:
            Список GUID типов связей (строки в id-пространстве ТИПОВ связей). Пустой
            список — специальных типов связей замещения нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.substitute_relation_type_guids()
                print(len(guids))

        Notes:
            operationId ``Metadata_GetSpecialSubstitutesRelationGuids``; путь
            ``GET /core/api/metadata/substitution/relationTypes/guids`` (ответ — массив
            строк). Связанные методы: :meth:`substitute_relation_type_ids`,
            :meth:`relation_type_has_substitutes_by_guid`.
        """
        path = "/core/api/metadata/substitution/relationTypes/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
