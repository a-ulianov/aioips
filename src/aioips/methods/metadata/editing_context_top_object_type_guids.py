"""Метод получения GUID верхнеуровневых типов объектов контекста редактирования."""

from ...core import APIManager


class EditingContextTopObjectTypeGuidsMixin(APIManager):
    """Реализует ``GET /core/api/metadata/editingContext/topObjectTypes/guids``."""

    async def editing_context_top_object_type_guids(
        self: "EditingContextTopObjectTypeGuidsMixin",
    ) -> list[str]:
        """Возвращает GUID верхнеуровневых (корневых) типов контекста редактирования.

        Контекст редактирования — набор типов объектов, правящихся совместно; внутри него
        есть корневые (главные) типы, с которых начинается совместная правка, и подчинённые.
        Метод отдаёт плоский перечень стабильных GUID только КОРНЕВЫХ типов — тех, чей
        объект инициирует контекст при checkout. GUID переносимы между установками IPS
        (в отличие от ``id``). Ответ сервера — массив строк, без обёртки
        ``...NullableResultDto``.

        Когда применять: чтобы по стабильному ключу определить типы — «точки входа» в
        совместное редактирование, сравнивая их между средами. Полный набор вовлечённых
        типов — :meth:`editing_context_object_type_guids`; перечень числовых id —
        :meth:`editing_context_top_object_type_ids`.

        Returns:
            Список GUID корневых типов объектов (строки в id-пространстве ТИПОВ объектов).
            Пустой список — корневых типов контекста редактирования нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.editing_context_top_object_type_guids()
                print(len(guids))

        Notes:
            operationId ``Metadata_GetEditingContextTopObjectGuids``; путь
            ``GET /core/api/metadata/editingContext/topObjectTypes/guids`` (ответ — массив
            строк). Связанные методы: :meth:`editing_context_top_object_type_ids`,
            :meth:`editing_context_object_type_guids`.
        """
        path = "/core/api/metadata/editingContext/topObjectTypes/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
