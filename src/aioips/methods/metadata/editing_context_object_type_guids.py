"""Метод получения GUID типов объектов контекста редактирования."""

from ...core import APIManager


class EditingContextObjectTypeGuidsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/editingContext/objectTypes/guids``."""

    async def editing_context_object_type_guids(
        self: "EditingContextObjectTypeGuidsMixin",
    ) -> list[str]:
        """Возвращает GUID всех типов объектов, входящих в контексты редактирования.

        Контекст редактирования — набор типов объектов, которые в IPS правятся совместно
        в одной транзакции/сессии (главный объект и подчинённые правятся как единое целое).
        Метод отдаёт плоский перечень стабильных GUID всех типов объектов, участвующих
        хотя бы в одном контексте редактирования. GUID переносимы между установками IPS
        (в отличие от ``id``), поэтому подходят для сверки конфигурации между средами.
        Ответ сервера — массив строк, без обёртки ``...NullableResultDto``.

        Когда применять: для сравнения наборов типов, вовлечённых в совместное
        редактирование, между средами по стабильным GUID. Перечень числовых id —
        :meth:`editing_context_object_type_ids`; только корневые типы —
        :meth:`editing_context_top_object_type_guids`.

        Returns:
            Список GUID типов объектов (строки в id-пространстве ТИПОВ объектов). Пустой
            список — ни один тип не входит в контексты редактирования.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.editing_context_object_type_guids()
                print(len(guids))

        Notes:
            operationId ``Metadata_GetEditingContextObjectGuids``; путь
            ``GET /core/api/metadata/editingContext/objectTypes/guids`` (ответ — массив
            строк). Связанные методы: :meth:`editing_context_object_type_ids`,
            :meth:`editing_context_top_object_type_guids`.
        """
        path = "/core/api/metadata/editingContext/objectTypes/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
