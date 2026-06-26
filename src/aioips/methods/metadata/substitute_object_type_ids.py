"""Метод получения id типов объектов, участвующих в замещении."""

from ...core import APIManager


class SubstituteObjectTypeIdsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/substitution/objectTypes/ids``."""

    async def substitute_object_type_ids(
        self: "SubstituteObjectTypeIdsMixin",
    ) -> list[int]:
        """Возвращает id всех типов объектов, участвующих в замещении.

        Замещение — механизм IPS, в котором один объект замещает другой через специальные
        связи замещения (например, замена детали аналогом). Метод отдаёт плоский перечень
        числовых ``id`` всех типов объектов, для которых определены отношения замещения.
        Ответ сервера — массив целых чисел, без обёртки ``...NullableResultDto``.

        Когда применять: для инвентаризации типов объектов, вовлечённых в замещения, перед
        обходом связей замещения. Проверка конкретного типа — :meth:`object_type_has_substitution`;
        перечень GUID — :meth:`substitute_object_type_guids`; типы связей замещения —
        :meth:`substitute_relation_type_ids`.

        Returns:
            Список id типов объектов (id-пространство ТИПОВ объектов метаданных). Пустой
            список — типов объектов с замещением нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.substitute_object_type_ids()
                print(len(ids))

        Notes:
            operationId ``Metadata_GetSubstituteObjectIds``; путь
            ``GET /core/api/metadata/substitution/objectTypes/ids`` (ответ — массив
            ``int``). Связанные методы: :meth:`substitute_object_type_guids`,
            :meth:`object_type_has_substitution`, :meth:`substitute_relation_type_ids`.
        """
        path = "/core/api/metadata/substitution/objectTypes/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
