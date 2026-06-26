"""Метод получения id типов объектов контекста редактирования."""

from ...core import APIManager


class EditingContextObjectTypeIdsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/editingContext/objectTypes/ids``."""

    async def editing_context_object_type_ids(
        self: "EditingContextObjectTypeIdsMixin",
    ) -> list[int]:
        """Возвращает id всех типов объектов, входящих в контексты редактирования.

        Контекст редактирования — набор типов объектов, которые в IPS правятся совместно
        в одной транзакции/сессии (главный объект и его подчинённые правятся как единое
        целое). Метод отдаёт плоский перечень числовых ``id`` всех типов объектов, которые
        участвуют хотя бы в одном контексте редактирования. Ответ сервера — массив целых
        чисел, без обёртки ``...NullableResultDto``.

        Когда применять: для инвентаризации типов, вовлечённых в совместное редактирование,
        чтобы заранее знать, какие типы будут затронуты при checkout главного объекта.
        Только верхнеуровневые (корневые) типы — :meth:`editing_context_top_object_type_ids`;
        перечень GUID — :meth:`editing_context_object_type_guids`.

        Returns:
            Список id типов объектов (id-пространство ТИПОВ объектов метаданных). Пустой
            список — ни один тип не входит в контексты редактирования.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.editing_context_object_type_ids()
                print(len(ids))

        Notes:
            operationId ``Metadata_GetEditingContextObjectIds``; путь
            ``GET /core/api/metadata/editingContext/objectTypes/ids`` (ответ — массив
            ``int``). Связанные методы: :meth:`editing_context_object_type_guids`,
            :meth:`editing_context_top_object_type_ids`.
        """
        path = "/core/api/metadata/editingContext/objectTypes/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
