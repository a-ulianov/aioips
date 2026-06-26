"""Метод оптимизации набора дочерних типов (свёртка к минимальному покрытию)."""

from ...core import APIManager


class OptimizeChildObjectTypesMixin(APIManager):
    """Реализует ``POST .../objectTypeTree/optimizeChildObjectTypes``."""

    async def optimize_child_object_types(
        self: "OptimizeChildObjectTypesMixin",
        object_type_ids: list[int],
    ) -> list[int]:
        """Сворачивает набор дочерних типов до минимального эквивалентного покрытия.

        Принимает список id типов и возвращает оптимизированный (сокращённый) набор: из
        входа удаляются типы, уже покрытые своими предками, присутствующими в наборе (если
        родительский тип задан, его потомков в наборе можно опустить — они подразумеваются
        рекурсивно). Результат задаёт то же множество объектов меньшим числом типов. Операция
        ЧТЕНИЯ метамодели: ничего не изменяет, лишь вычисляет покрытие; POST используется для
        передачи списка телом.

        Когда применять: перед сохранением/передачей правил применяемости или фильтров по
        типам, чтобы не хранить избыточные подтипы; для нормализации пользовательского
        выбора типов. Рекурсивное разворачивание в обратную сторону —
        :meth:`object_type_children_ids_recursive_by_ids`.

        Args:
            object_type_ids: Список id ТИПОВ объектов (``ObjectTypeID``; локальные) для
                оптимизации. Передаётся телом запроса (JSON-массив).

        Returns:
            Сокращённый список id ТИПОВ (``ObjectTypeID``), эквивалентный входному по
            покрытию. Пустой список — входной список пуст.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                # 1700 — родитель 1742; результат свернётся к [1700].
                minimal = await ips.optimize_child_object_types([1700, 1742])
                print(minimal)

        Notes:
            operationId ``Metadata_OptimizeChildObjectTypes``; путь
            ``POST /core/api/metadata/objectTypeTree/optimizeChildObjectTypes`` (тело —
            ``list[int]``; ответ — массив ``int``). См. объектной модели IPS. Связанные
            методы: :meth:`object_type_children_ids_recursive_by_ids`.
        """
        path = "/core/api/metadata/objectTypeTree/optimizeChildObjectTypes"
        data = await self._request("post", path, json=object_type_ids)
        return [int(item) for item in data] if data is not None else []
