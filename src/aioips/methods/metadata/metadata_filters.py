"""Метод получения фильтров метаданных по списку имён."""

from typing import Any

from ...core import APIManager


class MetadataFiltersMixin(APIManager):
    """Реализует ``POST /core/api/metadata/filters`` (``Metadata_GetMetadataFilters``)."""

    async def metadata_filters(
        self: "MetadataFiltersMixin",
        names: list[str],
    ) -> dict[str, Any]:
        """Возвращает именованные фильтры метамодели как словарь «имя → список id типов».

        Резолвит набор серверных фильтров метаданных по их строковым именам в наборы
        идентификаторов типов. Каждый фильтр (ключ результата) разворачивается в список
        ``id`` ТИПОВ объектов, которые он отбирает. Операция ЧТЕНИЯ: POST применяется лишь
        для передачи списка имён телом, метамодель не изменяется. Ключи в ответе НЕ
        приводятся к camelCase (сервер сохраняет исходный регистр имён фильтров).

        Когда применять: когда конфигурация/UI оперирует именованными фильтрами типов, а в
        коде нужны конкретные id для последующей выборки или проверки применяемости.

        Args:
            names: Список имён фильтров метаданных (как заданы на сервере). Передаётся телом
                запроса (JSON-массив строк). Имена, которым нет соответствия, в результат не
                попадут.

        Returns:
            Словарь ``{имя_фильтра: list[int]}``, где значение — список id ТИПОВ объектов
            (``ObjectTypeID``), отбираемых фильтром. Пустой словарь — ни одно имя не
            разрешилось.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                filters = await ips.metadata_filters(["Документы", "Изделия"])
                doc_type_ids = filters.get("Документы", [])

        Notes:
            operationId ``Metadata_GetMetadataFilters``; путь
            ``POST /core/api/metadata/filters`` (тело — ``list[str]``; ответ — объект-словарь
            ``{string: list[int]}``). См. [[ips-object-model]].
        """
        data = await self._request("post", "/core/api/metadata/filters", json=names)
        return data if isinstance(data, dict) else {}
