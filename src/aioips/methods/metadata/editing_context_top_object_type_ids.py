"""Метод получения id верхнеуровневых типов объектов контекста редактирования."""

from ...core import APIManager


class EditingContextTopObjectTypeIdsMixin(APIManager):
    """Реализует ``GET /core/api/metadata/editingContext/topObjectTypes/ids``."""

    async def editing_context_top_object_type_ids(
        self: "EditingContextTopObjectTypeIdsMixin",
    ) -> list[int]:
        """Возвращает id верхнеуровневых (корневых) типов контекста редактирования.

        Контекст редактирования — набор типов объектов, правящихся совместно; внутри него
        есть корневые (главные) типы, с которых начинается совместная правка, и подчинённые.
        Метод отдаёт плоский перечень числовых ``id`` только КОРНЕВЫХ типов — тех, чей
        объект инициирует контекст при checkout. Ответ сервера — массив целых чисел, без
        обёртки ``...NullableResultDto``.

        Когда применять: чтобы определить, какие типы объектов выступают «точкой входа» в
        совместное редактирование (главный объект). Полный набор всех вовлечённых типов
        (корневые + подчинённые) — :meth:`editing_context_object_type_ids`; перечень GUID —
        :meth:`editing_context_top_object_type_guids`.

        Returns:
            Список id корневых типов объектов (id-пространство ТИПОВ объектов). Пустой
            список — корневых типов контекста редактирования нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.editing_context_top_object_type_ids()
                print(len(ids))

        Notes:
            operationId ``Metadata_GetEditingContextTopObjectIds``; путь
            ``GET /core/api/metadata/editingContext/topObjectTypes/ids`` (ответ — массив
            ``int``). Связанные методы: :meth:`editing_context_top_object_type_guids`,
            :meth:`editing_context_object_type_ids`.
        """
        path = "/core/api/metadata/editingContext/topObjectTypes/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
