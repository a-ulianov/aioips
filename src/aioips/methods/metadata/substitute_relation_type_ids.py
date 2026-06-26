"""Метод получения id специальных типов связей замещения."""

from ...core import APIManager


class SubstituteRelationTypeIdsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/substitution/relationTypes/ids``."""

    async def substitute_relation_type_ids(
        self: "SubstituteRelationTypeIdsMixin",
    ) -> list[int]:
        """Возвращает id всех специальных типов связей замещения.

        Замещение реализуется через специальные типы СВЯЗЕЙ: объект-заместитель связан с
        замещаемым объектом связью особого типа. Метод отдаёт плоский перечень числовых
        ``id`` всех таких типов связей замещения. Ответ сервера — массив целых чисел, без
        обёртки ``...NullableResultDto``.

        Когда применять: чтобы знать, какими типами связей выражается замещение (например,
        для фильтрации связей объекта по типу). Проверка конкретного типа связи —
        :meth:`relation_type_has_substitutes`; перечень GUID —
        :meth:`substitute_relation_type_guids`; типы объектов с замещением —
        :meth:`substitute_object_type_ids`.

        Returns:
            Список id типов связей (id-пространство ТИПОВ связей метаданных). Пустой
            список — специальных типов связей замещения нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.substitute_relation_type_ids()
                print(len(ids))

        Notes:
            operationId ``Metadata_GetSpecialSubstitutesRelationIds``; путь
            ``GET /core/api/metadata/substitution/relationTypes/ids`` (ответ — массив
            ``int``). Связанные методы: :meth:`substitute_relation_type_guids`,
            :meth:`relation_type_has_substitutes`.
        """
        path = "/core/api/metadata/substitution/relationTypes/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
